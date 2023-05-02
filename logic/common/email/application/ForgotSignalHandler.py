from dependency_injector.wiring import inject, Provide
from src.common_container import CommonContainer

from logic.common.email.application.port.outgoing.EmailSender import EmailSender

from blinker import signal

forgot_signal = signal('forgot-signal')


@forgot_signal.connect_via('auth_email')
@inject
def signup_auth_signal_handler(sender, email, auth_code,
                               email_sender: EmailSender = Provide[CommonContainer.email_sender]):

    subject = '[왔소] 비밀번호 찾기 인증코드입니다.'
    body = f'인증코드 : {auth_code}'

    email_sender.send(email, subject, body)


@forgot_signal.connect_via('username')
@inject
def signup_auth_signal_handler(sender, email, username,
                               email_sender: EmailSender = Provide[CommonContainer.email_sender]):

    subject = '[왔소] 아이디 찾기 결과입니다.'
    body = f'아이디 : {username}'

    email_sender.send(email, subject, body)