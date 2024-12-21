import os
import smtplib
import zipfile
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tqdm import tqdm  # Progress bar

# تعريف الامتدادات التي سيتم البحث عنها
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
PROCESSED_FILES_LOG = "processed_files.log"

def find_files(root_dir):
    """البحث عن الملفات داخل مجلد معين"""
    files = []
    total_size = 0
    for root, dirs, files_in_dir in os.walk(root_dir):
        for file in files_in_dir:
            file_path = os.path.join(root, file)
            if file.lower().endswith(tuple(IMAGE_EXTENSIONS)) and os.path.exists(file_path):
                files.append(file_path)
                total_size += os.path.getsize(file_path)
    return files, total_size / (1024 * 1024)  # الحجم الكلي بالميجابايت

def load_processed_files(log_file):
    """تحميل الملفات التي تم معالجتها مسبقًا"""
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return set(f.read().splitlines())
    return set()

def save_processed_file(log_file, file_path):
    """حفظ اسم الملف الذي تم معالجته في السجل"""
    with open(log_file, 'a') as f:
        f.write(file_path + '\n')

def create_and_send_zip(files, max_size_mb, index, sender_email, sender_password, recipient_email):
    """إنشاء ملفات ZIP وإرسالها بالبريد الإلكتروني"""
    current_zip = []
    current_size = 0

    # تحميل الملفات المعالجة مسبقًا
    processed_files = load_processed_files(PROCESSED_FILES_LOG)

    with tqdm(total=len(files), desc=f"Processing zip {index}", unit="file") as pbar:
        for file in files:
            if file in processed_files or not os.path.exists(file):  # تخطي الملفات المعالجة أو غير الموجودة
                pbar.update(1)
                continue
            
            file_size = os.path.getsize(file) / (1024 * 1024)  # الحجم بالميجابايت
            if current_size + file_size > max_size_mb:
                zip_name = f"files_part{index}.zip"
                with zipfile.ZipFile(zip_name, 'w') as zipf:
                    for f in current_zip:
                        zipf.write(f, os.path.basename(f))
                send_email(sender_email, sender_password, recipient_email, 
                           f"File Part {index}", "Please find the attached file.", [zip_name])
                # حفظ الملفات في السجل
                for f in current_zip:
                    save_processed_file(PROCESSED_FILES_LOG, f)
                # إعادة تعيين المتغيرات
                current_zip = []
                current_size = 0
                index += 1
            current_zip.append(file)
            current_size += file_size
            pbar.update(1)

        if current_zip:
            zip_name = f"files_part{index}.zip"
            with zipfile.ZipFile(zip_name, 'w') as zipf:
                for f in current_zip:
                    zipf.write(f, os.path.basename(f))
            send_email(sender_email, sender_password, recipient_email, 
                       f"File Part {index}", "Please find the attached file.", [zip_name])
            for f in current_zip:
                save_processed_file(PROCESSED_FILES_LOG, f)
            pbar.update(len(current_zip))

def send_email(sender_email, sender_password, recipient_email, subject, body, attachments):
    """إرسال البريد الإلكتروني مع المرفقات"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for attachment_path in attachments:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully: {attachments}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # المستخدم يجب أن يملأ هذه المتغيرات بنفسه
    ROOT_DIR = input("Enter the root directory to scan: ")  # المجلد الرئيسي
    SENDER_EMAIL = input("Enter sender email: ")  # بريد المرسل
    SENDER_PASSWORD = input("Enter sender password: ")  # كلمة مرور المرسل
    RECIPIENT_EMAIL = input("Enter recipient email: ")  # بريد المستلم

    print("Scanning...")
    start_time = time.time()
    files, total_size = find_files(ROOT_DIR)

    if not files:
        print("No files found.")
    else:
        print(f"Count: {len(files)}, Total size: {total_size:.2f} MB.")
        print("Processing and sending files...")

        # معالجة وإرسال الملفات
        create_and_send_zip(files, max_size_mb=23, index=1, 
                            sender_email=SENDER_EMAIL, 
                            sender_password=SENDER_PASSWORD, 
                            recipient_email=RECIPIENT_EMAIL)

    end_time = time.time()
    print("Done Done.")
