import smtplib
from email.mime.text import MIMEText
import random

def compose_email(username,recipient):
    verification_code = random.randint(100000,999999)
    subject = "Verify Your Email | FAST-NUCES TMS"
    body = f'''
    Hi Abdur Razzaq,

    We received a request to verify your email address.

    {verification_code}

    Enter this code to complete the verification. The code will expire in 5 minutes.'''

    sender = "k213200@nu.edu.pk"
    recipients = recipient
    password = "aglmaitmvcdgmypa"
    if(send_email(subject, body, sender, recipients, password)):
        return verification_code

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
    return True