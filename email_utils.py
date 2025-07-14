import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, body):
    sender_email = "23nidheesingh@gmail.com"
    sender_password = "mtal opwv ijfh upjw"  # Use App Password if using Gmail

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False
