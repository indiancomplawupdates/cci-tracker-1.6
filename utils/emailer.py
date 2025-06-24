import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.fortune_cookies import get_fortune
from config import EMAIL_ADDRESS, EMAIL_PASSWORD
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

def send_update_email(to_email, updates):
    template = env.get_template("email_update.html")
    html = template.render(email=to_email, updates=updates)
    send_email(to_email, "🧾 New CCI Order(s) Alert!", html)

def send_fortune_email(to_email):
    template = env.get_template("email_fortune.html")
    html = template.render(email=to_email, fortune=get_fortune())
    send_email(to_email, "🔮 Your CCI Fortune Cookie", html)

def send_email(to_email, subject, html):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
