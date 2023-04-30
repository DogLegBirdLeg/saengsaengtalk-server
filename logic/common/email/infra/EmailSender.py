from logic.common.email.use_case.IEmailSender import IEmailSender
import smtplib
from email.mime.text import MIMEText
from config.production.email import sender_email, code
from multiprocessing import Process


class EmailProcess(Process):
    def __init__(self, to_email, subject, body):
        self.from_email = sender_email
        self.to_email = to_email
        self.subject = subject
        self.body = body
        Process.__init__(self)

    def run(self):
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp.starttls()
        self.smtp.login(sender_email, code)

        msg = MIMEText(self.body)
        msg['Subject'] = self.subject

        self.smtp.sendmail(self.from_email, self.to_email, msg.as_string())
        self.smtp.quit()


class EmailSender(IEmailSender):
    def send_auth_code(self, email, auth_code) -> str:
        subject = '인증코드'
        body = f'인증코드 : {auth_code}'
        EmailProcess(email, subject, body).start()
        return auth_code

    def send_username(self, email, username):
        subject = '아이디'
        body = f'아이디 : {username}'
        EmailProcess(email, subject, body).start()
