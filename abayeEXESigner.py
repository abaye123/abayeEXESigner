# abaye EXE Signer v1.3.0
# Date: 22/05/2025
# Email: cs@abaye.co
# GitHub: github.com/abaye123
# Sign icon by Icons8

import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from dotenv import load_dotenv
import shutil
import webbrowser
import configparser

load_dotenv()

def get_script_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

script_directory = get_script_directory()
config_file_path = os.path.join(script_directory, 'config.ini')

# הגדרות ברירת מחדל מ-.env
CERT_PATH = os.getenv('CERT_PATH', os.path.join(script_directory, 'Cert.pfx'))
PASSWORD = os.getenv('PASSWORD')
TIMESTAMP_SERVER = os.getenv('TIMESTAMP_SERVER', 'http://timestamp.digicert.com')
SIGTOOL_PATH = os.getenv('SIGTOOL_PATH', os.path.join(script_directory, 'signtool', 'signtool.exe'))
ORG_SIGNED = os.getenv('ORG_SIGNED', 'abaye ai')

def load_config():
    """טעינת הקונפיגורציה מקובץ INI"""
    config = configparser.ConfigParser()
    
    # ערכי ברירת מחדל
    default_config = {
        'signing_mode': 'copy',
        'auto_delete_original': 'False',
        'auto_delete_backup': 'False',
        'window_width': '820',
        'window_height': '680'
    }
    
    if os.path.exists(config_file_path):
        try:
            config.read(config_file_path, encoding='utf-8')
            if 'Preferences' in config:
                # מיזוג עם ערכי ברירת מחדל
                loaded_config = dict(default_config)
                loaded_config.update(dict(config['Preferences']))
                return loaded_config
        except Exception as e:
            print(f"שגיאה בטעינת הקונפיגורציה: {e}")
    
    return default_config

def save_config():
    """שמירת הקונפיגורציה לקובץ INI"""
    config = configparser.ConfigParser()
    config['Preferences'] = {
        'signing_mode': signing_mode_var.get(),
        'auto_delete_original': str(auto_delete_original.get()),
        'auto_delete_backup': str(auto_delete_backup.get()),
        'window_width': str(app.winfo_width()),
        'window_height': str(app.winfo_height())
    }
    
    try:
        with open(config_file_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    except Exception as e:
        log_message(f"שגיאה בשמירת הקונפיגורציה: {e}")

def apply_config(config_data):
    """הפעלת הגדרות הקונפיגורציה"""
    signing_mode_var.set(config_data['signing_mode'])
    auto_delete_original.set(config_data['auto_delete_original'] == 'True')
    auto_delete_backup.set(config_data['auto_delete_backup'] == 'True')
    
    # גודל חלון
    try:
        width = int(config_data['window_width'])
        height = int(config_data['window_height'])
        app.geometry(f"{width}x{height}")
    except ValueError:
        app.geometry("800x650")
    
    # עדכון מצב הכפתורים
    toggle_delete_options()

def check_signatures(file_path):
    """בדיקת חתימות הקובץ באמצעות signtool."""
    try:
        # הרצת פקודת signtool לבדיקת חתימות
        command = [SIGTOOL_PATH, 'verify', '/pa', '/v', file_path]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        
        log_message(f"תוצאות בדיקת החתימות עבור הקובץ '{file_path}':")
        
        # בדיקה אם יש חתימה תקפה
        if ORG_SIGNED in result.stdout:
            log_message("נמצאה חתימה תקפה.\n")
            return True
        else:
            log_message("לא נמצאה חתימה תקפה.\n")
            return False

    except subprocess.CalledProcessError as e:
        log_message(f"שגיאה בבדיקת החתימות: {str(e)}")
        return False

def sign_exe(file_path, signing_mode):
    """חתימת הקובץ הניתן להרצה."""
    original_file = file_path
    
    if signing_mode == "copy":
        # יצירת עותק עם סיומת _signed
        base, ext = os.path.splitext(file_path)
        target_file = f"{base}_signed{ext}"
        shutil.copy2(file_path, target_file)
    elif signing_mode == "original":
        # חתימה ישירות על הקובץ המקורי
        target_file = file_path
    elif signing_mode == "replace":
        # יצירת עותק זמני, חתימה וחזרה לשם המקורי
        base, ext = os.path.splitext(file_path)
        temp_file = f"{base}_temp{ext}"
        backup_file = f"{base}_backup{ext}"
        
        # יצירת גיבוי של הקובץ המקורי
        shutil.copy2(file_path, backup_file)
        # יצירת עותק זמני לחתימה
        shutil.copy2(file_path, temp_file)
        target_file = temp_file

    # בניית פקודה לחתימת הקובץ הניתן להרצה
    command = [
        SIGTOOL_PATH, 
        'sign', 
        '/f', CERT_PATH, 
        '/fd', 'SHA256', 
        '/td', 'SHA256', 
        '/tr', TIMESTAMP_SERVER, 
        '/d', "Signed Executable",
        target_file
    ]
    
    # הוספת פרמטר סיסמה רק אם קיימת סיסמה
    if PASSWORD and PASSWORD.strip():
        command.insert(4, '/p')  # הוספת פרמטר /p אחרי /f CERT_PATH
        command.insert(5, PASSWORD)  # הוספת הסיסמה

    try:
        # הרצת פקודת signtool
        result = subprocess.run(command, capture_output=True, text=True)
        log_message(f"חותם {target_file}...\n{result.stdout}\n{result.stderr}")

        if result.returncode == 0:
            if signing_mode == "replace":
                # החלפת הקובץ המקורי בקובץ החתום
                try:
                    os.remove(original_file)  # מחיקת הקובץ המקורי
                    os.rename(temp_file, original_file)  # שינוי שם הקובץ החתום
                    
                    # מחיקת הגיבוי אם הכל הצליח והמשתמש ביקש
                    if auto_delete_backup.get():
                        os.remove(backup_file)
                        log_message(f"הגיבוי נמחק אוטומטית: {backup_file}")
                    else:
                        log_message(f"גיבוי נשמר: {backup_file}")
                    
                    log_message(f"החתימה הושלמה בהצלחה: {original_file}")
                    return original_file
                except Exception as e:
                    # במקרה של שגיאה, החזרת הגיבוי
                    if os.path.exists(backup_file):
                        if os.path.exists(original_file):
                            os.remove(original_file)
                        os.rename(backup_file, original_file)
                    log_message(f"שגיאה בהחלפת הקובץ, הגיבוי הוחזר: {str(e)}")
                    return None
            else:
                log_message(f"החתימה הושלמה בהצלחה: {target_file}")
                
                # מחיקת הקובץ המקורי אם נבחרה האפשרות
                if signing_mode == "copy" and auto_delete_original.get():
                    try:
                        os.remove(original_file)
                        log_message(f"הקובץ המקורי נמחק אוטומטית: {original_file}")
                    except Exception as e:
                        log_message(f"שגיאה במחיקת הקובץ המקורי: {str(e)}")
                
                return target_file
        else:
            log_message(f"החתימה נכשלה: {result.stderr}")
            
            # ניקוי קבצים זמניים במקרה של כשלון
            if signing_mode == "copy" and os.path.exists(target_file):
                os.remove(target_file)
            elif signing_mode == "replace":
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                if os.path.exists(backup_file):
                    os.remove(backup_file)
            
            return None

    except Exception as e:
        log_message(f"שגיאה במהלך החתימה: {str(e)}")
        
        # ניקוי קבצים זמניים במקרה של חריגה
        if signing_mode == "copy" and os.path.exists(target_file):
            os.remove(target_file)
        elif signing_mode == "replace":
            if os.path.exists(temp_file):
                os.remove(temp_file)
            if os.path.exists(backup_file):
                os.remove(backup_file)
        
        return None

def log_message(message):
    log_box.configure(state='normal')
    log_box.insert(tk.END, message + '\n')
    log_box.configure(state='disabled')
    log_box.see(tk.END)

def clear_log():
    log_box.configure(state='normal')
    log_box.delete('1.0', tk.END)
    log_box.configure(state='disabled')

def select_file_for_signing():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
    if file_path:
        current_file = file_path
        is_signed = check_signatures(current_file)
        sign_anyway_button.configure(state='normal')
        if not is_signed:
            sign_file()

def select_file_for_checking():
    file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
    if file_path:
        check_signatures(file_path)

def sign_file():
    if current_file:
        # קבלת מצב החתימה הנבחר
        signing_mode = signing_mode_var.get()
        
        signed_file_path = sign_exe(current_file, signing_mode)
        if signed_file_path:
            messagebox.showinfo("הצלחה", f"הקובץ נחתם: {signed_file_path}")
            check_signatures(signed_file_path)

def open_website(event):
    webbrowser.open_new("https://abaye.co")

def toggle_delete_options():
    """הפעלה/כיבוי של אפשרויות המחיקה בהתאם לבחירת מצב החתימה"""
    mode = signing_mode_var.get()
    
    if mode == "copy":
        auto_delete_original_check.configure(state='normal')
        auto_delete_backup_check.configure(state='disabled')
    elif mode == "replace":
        auto_delete_original_check.configure(state='disabled')
        auto_delete_backup_check.configure(state='normal')
    else:  # original
        auto_delete_original_check.configure(state='disabled')
        auto_delete_backup_check.configure(state='disabled')
    
    # שמירת הקונפיגורציה בכל שינוי
    save_config()

def on_closing():
    """פונקציה שמופעלת בעת סגירת התוכנה"""
    save_config()
    app.destroy()

def on_config_change():
    """פונקציה שמופעלת כאשר משתנה הקונפיגורציה"""
    save_config()

# יצירת חלון ראשי
app = ttk.Window(themename="darkly")
app.title("EXE Signer")
app.protocol("WM_DELETE_WINDOW", on_closing)

# טעינת הקונפיגורציה
config_data = load_config()

# כותרת
header_frame = ttk.Frame(app)
header_frame.pack(pady=10)

header_label = ttk.Label(header_frame, text="EXE Signer", font=("Helvetica", 20, "bold"))
header_label.pack()

version_label = ttk.Label(header_frame, text="by abaye v1.3.0", font=("Helvetica", 10))
version_label.pack()

# מסגרת אפשרויות חתימה
options_frame = ttk.LabelFrame(app, text="אפשרויות חתימה", padding=10)
options_frame.pack(pady=10, padx=20, fill='x')

# בחירת מצב חתימה
signing_mode_var = tk.StringVar(value="copy")

mode_frame = ttk.Frame(options_frame)
mode_frame.pack(fill='x', pady=5)

ttk.Label(mode_frame, text="מצב חתימה:", font=("Helvetica", 10, "bold")).pack(anchor='w')

copy_radio = ttk.Radiobutton(mode_frame, text="יצירת עותק עם סיומת _signed", 
                            variable=signing_mode_var, value="copy", 
                            command=lambda: [toggle_delete_options(), on_config_change()])
copy_radio.pack(anchor='w', padx=20)

original_radio = ttk.Radiobutton(mode_frame, text="חתימה ישירות על הקובץ המקורי", 
                                variable=signing_mode_var, value="original", 
                                command=lambda: [toggle_delete_options(), on_config_change()])
original_radio.pack(anchor='w', padx=20)

replace_radio = ttk.Radiobutton(mode_frame, text="החלפת הקובץ המקורי בקובץ החתום", 
                               variable=signing_mode_var, value="replace", 
                               command=lambda: [toggle_delete_options(), on_config_change()])
replace_radio.pack(anchor='w', padx=20)

# אפשרויות מחיקה אוטומטית
delete_frame = ttk.Frame(options_frame)
delete_frame.pack(fill='x', pady=10)

ttk.Label(delete_frame, text="אפשרויות מחיקה אוטומטית:", font=("Helvetica", 10, "bold")).pack(anchor='w')

auto_delete_original = tk.BooleanVar()
auto_delete_original_check = ttk.Checkbutton(delete_frame, text="מחק את הקובץ המקורי לאחר יצירת עותק חתום", 
                                           variable=auto_delete_original, state='normal',
                                           command=on_config_change)
auto_delete_original_check.pack(anchor='w', padx=20)

auto_delete_backup = tk.BooleanVar()
auto_delete_backup_check = ttk.Checkbutton(delete_frame, text="מחק את קובץ הגיבוי לאחר החלפה מוצלחת", 
                                         variable=auto_delete_backup, state='disabled',
                                         command=on_config_change)
auto_delete_backup_check.pack(anchor='w', padx=20)

# כפתורים
button_frame = ttk.Frame(app)
button_frame.pack(pady=20)

select_button = ttk.Button(button_frame, text="בחר קובץ EXE לחתימה", command=select_file_for_signing, style='primary.TButton')
select_button.pack(side=tk.LEFT, padx=5)

check_signatures_button = ttk.Button(button_frame, text="בדוק חתימות", command=select_file_for_checking, style='info.TButton')
check_signatures_button.pack(side=tk.LEFT, padx=5)

sign_anyway_button = ttk.Button(button_frame, text="חתום בכל זאת", command=sign_file, style='warning.TButton', state='disabled')
sign_anyway_button.pack(side=tk.LEFT, padx=5)

clear_log_button = ttk.Button(button_frame, text="נקה לוג", command=clear_log, style='secondary.TButton')
clear_log_button.pack(side=tk.LEFT, padx=5)

# תיבת הלוג
log_box = scrolledtext.ScrolledText(app, width=90, height=15, wrap=tk.WORD)
log_box.pack(pady=20, padx=20, fill='both', expand=True)

# תחתית
website_label = ttk.Label(app, text="abaye.co", cursor="hand2", font=("Helvetica", 10, "underline"))
website_label.pack(pady=5)
website_label.bind("<Button-1>", open_website)

icon_label = ttk.Label(app, text="Sign icon by Icons8", font=("Helvetica", 8))
icon_label.pack(pady=5)

# משתנה גלובלי לקובץ הנוכחי
current_file = None

# הפעלת הקונפיגורציה הנטענת
apply_config(config_data)

# הפעלת הממשק
app.mainloop()