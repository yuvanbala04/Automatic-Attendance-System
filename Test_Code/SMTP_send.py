import smtplib

EMAIL_SENDER = "ranjithp24072004@gmail.com"
EMAIL_PASSWORD = "fmdr wzyi tgms cgmk"  # Use App Password, not real password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Create SMTP session
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()  # Enable security
server.login(EMAIL_SENDER, EMAIL_PASSWORD)

# Send email
recipient = "yuvanbala2021@gmail.com"
subject = "Test Email"
body = "Hello, this is a test email from Python."

message = f"Subject: {subject}\n\n{body}"
server.sendmail(EMAIL_SENDER, recipient, message)
server.quit()

print("Email sent successfully!")
