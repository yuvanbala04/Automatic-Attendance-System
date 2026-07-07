import csv
import smtplib
from datetime import datetime
EMAIL_CSV_FILE = "emails.csv"  # CSV file containing names and emails
name = "YuvanBala"
def load_email_addresses():
    emails = {}
    with open(EMAIL_CSV_FILE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                name, email = row
                emails[name] = email
    return emails

email_dict = load_email_addresses()
EMAIL_SENDER = "ranjithp24072004@gmail.com"
EMAIL_PASSWORD = "fmdr wzyi tgms cgmk"  # Use App Password, not real password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(name):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    recipient = email_dict.get(name)
    if not recipient:
        print(f"No email found for {name}")
        return
    subject = "Attendance Logged"
    body = f"Dear {name},\n\nYour attendance has been recorded on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(EMAIL_SENDER, recipient, message)
    server.quit()
    print("Email sent successfully!")
send_email(name)