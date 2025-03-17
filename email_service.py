import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure Free SMTP Server (Brevo)
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USERNAME = "88207f002@smtp-brevo.com"
SMTP_PASSWORD = "V27WHUOwxr8dBhTJ"

def send_email(to_email, subject, message):
    """Send an email notification"""
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Email Error:", e)
        return False
