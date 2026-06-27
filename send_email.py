import smtplib
import socket
import ssl
from email.mime.text import MIMEText
from email.header import Header

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL, SMTP_SERVER, SMTP_PORT
from debug import debugger

sender = EMAIL_ADDRESS
password = EMAIL_PASSWORD
receivers = [RECIPIENT_EMAIL]
smtp_server = SMTP_SERVER
smtp_port = int(SMTP_PORT)

def check_email():
    if not debugger.check_func_status("check_email"):
        return True
    try:
        socket.create_connection((smtp_server, smtp_port), timeout=10)
    except Exception as e:
        return False
        
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            response = server.login(sender, password)
            return True
    except Exception as e:
        return False

def send_email(content, status=""):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = sender 
    msg['To'] = ", ".join(receivers)        
    msg['Subject'] = Header(f"Daily News Summary{status}", 'utf-8')
    server = None
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())
        return True
    except Exception as e:
        raise Exception(f"邮件发送失败: {e}")
    finally:
        if server:
            try:
                server.quit()
            except:
                pass  

def info(content):
    if not debugger.check_func_status("info"):
        return
    send_email(content)

def debugs(content):
    if not debugger.check_func_status("debugs"):
        return
    send_email(content, " - Debug")

def warn(content):
    if not debugger.check_func_status("warn"):
        return
    send_email(content, " - Warning")

def err(content):
    if not debugger.check_func_status("err"):
        return
    send_email(content, " - Error")
