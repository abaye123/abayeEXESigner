# abayeEXESigner

זהו יישום פייתון GUI לחתימת קבצי exe באמצעות הכלי [SignTool](https://github.com/Delphier/SignTool).

## התקנה והגדרה

לפני ההפעלה, יש להגדיר בקובץ `.env` את הערכים הבאים:

- **CERT_PATH**: קובץ תעודה מסוג `.pfx` מתאים, ניתן ליצור באמצעות רשויות מורשות או עצמאית באמצעות OpenSSL (ברירת מחדל קובץ בשם `cert.pfx` בתיקייה שבה נמצא היישום שלנו)
- **PASSWORD**: *חובה* סיסמת המפתח המתאימה לקובץ התעודה שנבחר
- **SIGTOOL_PATH**: מיקום שונה לתיקיית הSignTool (ברירת מחדל תיקייה בשם `SignTool` בתיקייה שבה נמצא היישום שלנו)
- **TIMESTAMP_SERVER**: שרת הזמן לאימות זמן החתימה. (ברירת מחדל זה `http://timestamp.digicert.com`)
- **ORG_SIGNED**: ערך סטרינג לחיפוש בתעודות, לזיהוי האם התוכנה כבר נחתמה על ידיכם, יכול להיות לדוגמה שם הארגון שלכם המופיע בתעודה

> **הערה:** יש בעיה בלוגיקה של בדיקה האם הקובץ כבר חתום, כך שלפעמים זה עשוי להחזיר תגובה שגויה.
> ניתן לבדוק חתימות בדרך נוספת באמצעות כניסה למאפייני הקובץ לשונית חתימות דיגטליות, אם הלשונית לא מופיעה, סימן שאין חתימה.

## שימוש

לאחר שסיימתם להגדיר את הכל, יש להקליק פעמיים על הקובץ `abayeEXESigner.exe` כדי להפעיל את התוכנה.

### דרישות נוספות

* אם אתם משתמשים בנטפרי, ייתכן שתצטרכו להפעיל את הקובץ הבא כמנהל בפעם הראשונה לפני שתפעילו את התוכנה כדי להגדיר את תעודת האבטחה של נטפרי:
[תוכנה להגדרה קלה של תעודת אבטחה של נטפרי בפייתון](https://github.com/abaye123/NetfreeSecurityCertificate/releases/tag/netfree)
[או לחצו כאן להדרכה בוויקי נטפרי](https://netfree.link/wiki/%D7%94%D7%AA%D7%A7%D7%A0%D7%AA_%D7%AA%D7%A2%D7%95%D7%93%D7%94_%D7%91%D7%A4%D7%99%D7%99%D7%AA%D7%95%D7%9F_-_%D7%A1%D7%A4%D7%A8%D7%99%D7%99%D7%AA_requests)

למשתמשי סינונים אחרים ברמת הרשת, אין לי מושג על השיטה, יש לפנות לשירות הלקוחות של חברת הסינון.

## תודות

* הפרויקט https://github.com/Delphier/SignTool
* אייקון היישום באדיבות האתר icons8.com
