from logic.common.email.use_case.IEmailSender import IEmailSender
import smtplib
from email.mime.text import MIMEText
from config.production.email import sender_email, code


class EmailSender(IEmailSender):
    def connection(self):
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtp.starttls()
        self.smtp.login(sender_email, code)

    def send_auth_code(self, email, auth_code) -> str:
        self.connection()
        msg = MIMEText(f'인증코드 : {auth_code}')
        msg['Subject'] = '인증코드'

        self.smtp.sendmail(sender_email, email, msg.as_string())
        self.smtp.quit()

        return auth_code

    def send_username(self, email, username):
        self.connection()
        msg = MIMEText(f'아이디 : {username}')
        msg['Subject'] = '아이디'

        self.smtp.sendmail('xoals3094@gmail.com', email, msg.as_string())
        self.smtp.quit()
