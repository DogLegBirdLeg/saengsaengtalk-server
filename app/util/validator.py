from app import exceptions
import re


def validate_name(name):
    r = re.fullmatch(r'^[a-zA-Z가-힣\s]{2,20}$', name)
    if r is None:
        raise exceptions.FormatError


def validate_username(username):
    r = re.fullmatch(r'^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{8,16}$', username)
    if r is None:
        raise exceptions.FormatError


def validate_password(password):
    r = re.fullmatch(r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~!@#$%^&])[a-zA-Z0-9~!@#$%^&]{8,16}$', password)
    if r is None:
        raise exceptions.FormatError


def validate_nickname(nickname):
    r = re.fullmatch(r'^[a-zA-Z가-힣0-9]{2,10}$', nickname)
    if r is None:
        raise exceptions.FormatError


def validate_account_number(account_number):
    r = re.fullmatch(r'^[a-zA-Z0-9가-힣-\s]{8,30}$', account_number)
    if r is None:
        raise exceptions.FormatError


def validate_email(email):
    r = re.fullmatch(r'^[a-zA-Z0-9]{2,20}@[a-zA-Z0-9.]{2,20}$', email)
    if r is None:
        raise exceptions.FormatError


def validate_auth_code(auth_code):
    r = re.fullmatch(r'^[0-9]{4}$', auth_code)
    if r is None:
        raise exceptions.FormatError
