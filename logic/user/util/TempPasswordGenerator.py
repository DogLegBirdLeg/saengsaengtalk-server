import random

LENGTH = 8
STRING_POOL = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_temp_password():
    temp_password = ""
    for i in range(LENGTH):
        temp_password += random.choice(STRING_POOL)

    return temp_password
