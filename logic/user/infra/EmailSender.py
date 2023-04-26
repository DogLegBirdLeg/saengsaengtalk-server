from logic.user.use_case.EmailSenderInterface import EmailSenderInterface
import random
import smtplib
from email.mime.text import MIMEText

LENGTH = 4
STRING_POOL = "0123456789"


class EmailSender(EmailSenderInterface):
    def send_auth_email(self, email) -> str:
        auth_code = ""
        for i in range(LENGTH):
            auth_code += random.choice(STRING_POOL)
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('xoals3094@gmail.com', 'sakagnjqdgotmkzv')
        msg = MIMEText(f'인증코드 : {auth_code}')
        msg['Subject'] = '인증코드'

        smtp.sendmail('xoals3094@gmail.com', email, msg.as_string())
        smtp.quit()

        return auth_code

    def send_username_email(self, email, username):
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('xoals3094@gmail.com', 'sakagnjqdgotmkzv')
        msg = MIMEText(f'아이디 : {username}')
        msg['Subject'] = '아이디'

        smtp.sendmail('xoals3094@gmail.com', email, msg.as_string())
        smtp.quit()
