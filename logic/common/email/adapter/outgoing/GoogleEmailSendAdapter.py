import smtplib
from email.mime.text import MIMEText
from config.production.email import sender_email, code

from logic.common.email.application.port.outgoing.EmailSender import EmailSender


class GoogleEmailSender(EmailSender):
    def __init__(self):
        self.from_email = sender_email
        self.app_code = code

    def connection(self):
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.from_email, self.app_code)
        return smtp

    def send(self, to, subject, body):
        smtp = self.connection()
        msg = MIMEText(body)
        msg['Subject'] = subject

        smtp.sendmail(self.from_email, to, msg.as_string())
        smtp.quit()
