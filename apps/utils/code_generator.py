import string
import random


def code_generator(n: int):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))