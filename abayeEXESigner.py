# abaye EXE Signer v1.2.2
# Date: 20/10/2024
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

load_dotenv()

def get_script_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

script_directory = get_script_directory()

# הגדרות ברירת מחדל מ-.env
CERT_PATH = os.getenv('CERT_PATH', os.path.join(script_directory, 'Cert.pfx'))
PASSWORD = os.getenv('PASSWORD')
TIMESTAMP_SERVER = os.getenv('TIMESTAMP_SERVER', 'http://timestamp.digicert.com')
SIGTOOL_PATH = os.getenv('SIGTOOL_PATH', os.path.join(script_directory, 'signtool', 'signtool.exe'))
ORG_SIGNED = os.getenv('ORG_SIGNED', 'abaye ai')

def check_signatures(file_path):
    """בדיקת חתימות הקובץ באמצעות signtool."""
    try:
        # הרצת פקודת signtool לבדיקת חתימות
        command = [SIGTOOL_PATH, 'verify', '/pa', '/v', file_path]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        
        log_message(f"תוצאות בדיקת החתימות עבור הקובץ '{file_path}':")
        #log_message(result.stdout)
        #log_message(result.stderr)
        
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

def sign_exe(file_path):
    """חתימת עותק של הקובץ הניתן להרצה."""
    base, ext = os.path.splitext(file_path)
    signed_file_path = f"{base}_signed{ext}"
    
    # יצירת עותק של הקובץ המקורי
    shutil.copy2(file_path, signed_file_path)

    # בניית פקודה לחתימת הקובץ הניתן להרצה
    command = [
        SIGTOOL_PATH, 
        'sign', 
        '/f', CERT_PATH, 
        '/fd', 'SHA256', 
        '/td', 'SHA256', 
        '/tr', TIMESTAMP_SERVER, 
        '/d', "Signed Executable",
        signed_file_path
    ]
    
    # הוספת פרמטר סיסמה רק אם קיימת סיסמה
    if PASSWORD and PASSWORD.strip():
        command.insert(4, '/p')  # הוספת פרמטר /p אחרי /f CERT_PATH
        command.insert(5, PASSWORD)  # הוספת הסיסמה

    try:
        # הרצת פקודת signtool
        result = subprocess.run(command, capture_output=True, text=True)
        log_message(f"חותם {signed_file_path}...\n{result.stdout}\n{result.stderr}")

        if result.returncode == 0:
            log_message(f"החתימה הושלמה בהצלחה: {signed_file_path}")
            return signed_file_path
        else:
            log_message(f"החתימה נכשלה: {result.stderr}")
            os.remove(signed_file_path)  # מחיקת העותק אם החתימה נכשלה
            return None

    except Exception as e:
        log_message(f"שגיאה במהלך החתימה: {str(e)}")
        os.remove(signed_file_path)  # מחיקת העותק אם אירעה חריגה
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
        signed_file_path = sign_exe(current_file)
        if signed_file_path:
            messagebox.showinfo("הצלחה", f"הקובץ נחתם: {signed_file_path}")
            check_signatures(signed_file_path)

def open_website(event):
    webbrowser.open_new("https://abaye.co")

app = ttk.Window(themename="darkly")
app.title("EXE Signer")
app.geometry("700x500")

header_frame = ttk.Frame(app)
header_frame.pack(pady=10)

header_label = ttk.Label(header_frame, text="EXE Signer", font=("Helvetica", 20, "bold"))
header_label.pack()

version_label = ttk.Label(header_frame, text="by abaye v1.2.2", font=("Helvetica", 10))
version_label.pack()

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

log_box = scrolledtext.ScrolledText(app, width=80, height=15, wrap=tk.WORD)
log_box.pack(pady=20)

website_label = ttk.Label(app, text="abaye.co", cursor="hand2", font=("Helvetica", 10, "underline"))
website_label.pack(pady=10)
website_label.bind("<Button-1>", open_website)

icon_label = ttk.Label(app, text="Sign icon by Icons8", font=("Helvetica", 8))
icon_label.pack(pady=10)

current_file = None

app.mainloop()