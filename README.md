# abayeEXESigner

**[עברית](#עברית) | [English](#english)**

---

## עברית

### סקירה כללית

abayeEXESigner הוא יישום GUI פשוט ואינטואיטיבי הכתוב בפייתון לחתימה דיגיטלית של קבצי EXE. התוכנה מספקת ממשק משתמש נוח לחתימת קבצים ניתנים להרצה באמצעות כלי SignTool של Microsoft, עם אפשרויות מתקדמות לניהול קבצים וחתימות.

### תכונות עיקריות

- **ממשק משתמש גרפי** - ממשק נוח ואינטואיטיבי בעברית
- **מספר מצבי חתימה** - בחירה בין יצירת עותק, חתימה ישירה או החלפת קובץ
- **בדיקת חתימות** - וידוא קיום חתימות דיגיטליות בקבצים
- **מחיקה אוטומטית** - אפשרויות מחיקה אוטומטית של קבצים מקוריים או גיבויים
- **לוג מפורט** - מעקב אחר כל הפעולות עם הודעות מפורטות
- **שמירת הגדרות** - שמירה אוטומטית של העדפות המשתמש

### דרישות מערכת

- Windows 10/11 (x64)
- .NET Framework 4.7.2 או גרסה חדשה יותר
- קובץ תעודה דיגיטלית (.pfx)
- Python 3.8+ (אם מריצים מקוד המקור)

### התקנה והגדרה

#### 1. הורדה
הורידו את הקובץ `abayeEXESigner.exe` מעמוד ה[Releases](https://github.com/abaye123/abayeEXESigner/releases).

#### 2. יצירת קובץ הגדרות
צרו קובץ `.env` באותה תיקייה שבה נמצא הקובץ הניתן להרצה:

```env
# נתיב לקובץ התעודה הדיגיטלית
CERT_PATH=C:\path\to\your\certificate.pfx

# סיסמה לקובץ התעודה (חובה!)
PASSWORD=your_certificate_password

# נתיב לכלי SignTool (אופציונלי)
SIGTOOL_PATH=C:\path\to\SignTool\signtool.exe

# שרת חותמת זמן (אופציונלי)
TIMESTAMP_SERVER=http://timestamp.digicert.com

# מחרוזת לזיהוי החתימה שלכם (אופציונלי)
ORG_SIGNED=Your Organization Name
```

#### 3. מבנה תיקיות
```
abayeEXESigner/
├── abayeEXESigner.exe
├── .env
├── cert.pfx (אופציונלי - אם לא מצויין נתיב אחר)
├── SignTool/ (מכיל את כלי SignTool)
│   ├── signtool.exe
│   └── ... (קבצי תמיכה נוספים)
└── config.ini (נוצר אוטומטית)
```

### מדריך שימוש

#### מצבי חתימה

1. **יצירת עותק עם סיומת _signed**
   - יוצר קובץ חדש עם הסיומת `_signed`
   - שומר על הקובץ המקורי ללא שינוי
   - אפשרות למחיקה אוטומטית של הקובץ המקורי

2. **חתימה ישירות על הקובץ המקורי**
   - חותם ישירות על הקובץ הקיים
   - משנה את הקובץ המקורי לצמיתות
   - מהיר ביותר אך בלתי הפיך

3. **החלפת הקובץ המקורי בקובץ החתום**
   - יוצר גיבוי של הקובץ המקורי
   - חותם ומחליף את הקובץ המקורי
   - אפשרות למחיקה אוטומטית של הגיבוי

#### תהליך החתימה

1. הפעילו את התוכנה
2. בחרו את מצב החתימה המועדף
3. הגדירו אפשרויות מחיקה אוטומטית (אופציונלי)
4. לחצו על "בחר קובץ EXE לחתימה"
5. בחרו את הקובץ הרצוי
6. התוכנה תבדוק אוטומטית אם הקובץ כבר חתום
7. אם הקובץ לא חתום - החתימה תתחיל אוטומטית
8. אם הקובץ כבר חתום - תוכלו לבחור "חתום בכל זאת"

#### בדיקת חתימות

- לחצו על "בדוק חתימות" לבדיקת קובץ ללא חתימה
- התוכנה תציג פרטים על החתימות הקיימות
- תקבלו הודעה אם הקובץ חתום על ידי הארגון שלכם

### פתרון בעיות

#### שגיאות נפוצות

**"Cannot find signtool.exe"**
- ודאו שתיקיית SignTool קיימת
- בדקו שהנתיב בקובץ .env נכון

**"Invalid certificate or password"**
- ודאו שקובץ התעודה קיים ונגיש
- בדקו שהסיסמה נכונה בקובץ .env

**"Timestamping failed"**
- בדקו חיבור לאינטרנט
- נסו להחליף את שרת חותמת הזמן

#### דרישות רשת

**למשתמשי נטפרי:**
- ייתכן שתצטרכו להתקין תעודת אבטחה של נטפרי
- השתמשו ב[כלי ההגדרה](https://github.com/abaye123/NetfreeSecurityCertificate/releases/tag/netfree)
- או עקבו אחר [המדריך בוויקי נטפרי](https://netfree.link/wiki/התקנת_תעודה_בפייתון_-_ספריית_requests)

**למשתמשי סינונים אחרים:**
- פנו לשירות הלקוחות של חברת הסינון

### קבצי הגדרות

#### config.ini
נוצר אוטומטית ושומר:
- מצב חתימה מועדף
- העדפות מחיקה אוטומטית
- גודל וממדי החלון

### פיתוח והרצה מקוד המקור

#### דרישות

```bash
pip install tkinter ttkbootstrap python-dotenv configparser
```

#### הרצה

```bash
python abayeEXESigner.py
```

#### בניית EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed abayeEXESigner.py
```

### רישיון

התוכנה מופצת תחת רישיון GPL v3. ראו קובץ LICENSE לפרטים.

### תודות

- פרויקט [SignTool](https://github.com/Delphier/SignTool) מאת Delphier
- אייקון היישום באדיבות [Icons8](https://icons8.com)
- פותח על ידי [abaye](https://abaye.co)

---

## English

### Overview

abayeEXESigner is a simple and intuitive Python GUI application for digitally signing EXE files. The software provides a user-friendly interface for signing executable files using Microsoft's SignTool, with advanced options for file and signature management.

### Key Features

- **Graphical User Interface** - Easy-to-use, intuitive interface
- **Multiple Signing Modes** - Choose between creating copy, direct signing, or file replacement
- **Signature Verification** - Verify existence of digital signatures in files
- **Automatic Deletion** - Auto-delete options for original files or backups
- **Detailed Logging** - Track all operations with comprehensive messages
- **Settings Persistence** - Automatic saving of user preferences

### System Requirements

- Windows 10/11 (x64)
- .NET Framework 4.7.2 or later
- Digital certificate file (.pfx)
- Python 3.8+ (if running from source)

### Installation and Setup

#### 1. Download
Download the `abayeEXESigner.exe` file from the [Releases](https://github.com/abaye123/abayeEXESigner/releases) page.

#### 2. Create Configuration File
Create a `.env` file in the same directory as the executable:

```env
# Path to digital certificate file
CERT_PATH=C:\path\to\your\certificate.pfx

# Certificate password (required!)
PASSWORD=your_certificate_password

# Path to SignTool (optional)
SIGTOOL_PATH=C:\path\to\SignTool\signtool.exe

# Timestamp server (optional)
TIMESTAMP_SERVER=http://timestamp.digicert.com

# String to identify your signature (optional)
ORG_SIGNED=Your Organization Name
```

#### 3. Directory Structure
```
abayeEXESigner/
├── abayeEXESigner.exe
├── .env
├── cert.pfx (optional - if no other path specified)
├── SignTool/ (contains SignTool utilities)
│   ├── signtool.exe
│   └── ... (additional support files)
└── config.ini (created automatically)
```

### Usage Guide

#### Signing Modes

1. **Create Copy with _signed Suffix**
   - Creates a new file with `_signed` suffix
   - Preserves original file unchanged
   - Option to auto-delete original file

2. **Sign Original File Directly**
   - Signs the existing file directly
   - Permanently modifies the original file
   - Fastest but irreversible

3. **Replace Original with Signed File**
   - Creates backup of original file
   - Signs and replaces the original file
   - Option to auto-delete backup

#### Signing Process

1. Launch the application
2. Select preferred signing mode
3. Configure auto-delete options (optional)
4. Click "Select EXE File for Signing"
5. Choose desired file
6. Software automatically checks if file is already signed
7. If file is unsigned - signing starts automatically
8. If file is already signed - you can choose "Sign Anyway"

#### Signature Verification

- Click "Check Signatures" to verify a file without signing
- Software displays details about existing signatures
- You'll get notification if file is signed by your organization

### Troubleshooting

#### Common Errors

**"Cannot find signtool.exe"**
- Ensure SignTool directory exists
- Check that path in .env file is correct

**"Invalid certificate or password"**
- Verify certificate file exists and is accessible
- Check password is correct in .env file

**"Timestamping failed"**
- Check internet connection
- Try changing timestamp server

#### Network Requirements

**For Netfree Users:**
- You may need to install Netfree security certificate
- Use the [setup tool](https://github.com/abaye123/NetfreeSecurityCertificate/releases/tag/netfree)
- Or follow the [Netfree wiki guide](https://netfree.link/wiki/התקנת_תעודה_בפייתון_-_ספריית_requests)

**For Other Network Filter Users:**
- Contact your filtering company's customer service

### Configuration Files

#### config.ini
Created automatically and saves:
- Preferred signing mode
- Auto-delete preferences
- Window size and dimensions

### Development and Running from Source

#### Requirements

```bash
pip install tkinter ttkbootstrap python-dotenv configparser
```

#### Running

```bash
python abayeEXESigner.py
```

#### Building EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed abayeEXESigner.py
```

### License

This software is distributed under GPL v3 license. See LICENSE file for details.

### Credits

- [SignTool](https://github.com/Delphier/SignTool) project by Delphier
- Application icon courtesy of [Icons8](https://icons8.com)
- Developed by [abaye](https://abaye.co)

---

## Contact

- **Website**: [abaye.co](https://abaye.co)
- **Email**: cs@abaye.co
- **GitHub**: [abaye123](https://github.com/abaye123)

## Version History

- **v1.3.0** (22/05/2025) - Current version with enhanced features and UI improvements