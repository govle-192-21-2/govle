from hashlib import pbkdf2_hmac
from os import urandom
from typing import Tuple

def hash_password(password: str) -> Tuple[str, str]:
    """
    Takes in a password, generates a random salt, and hashes the password
    with the salt.

    :param password: Password to be hashed
    :return: Tuple of hashed password and salt, both byte arrays encoded as hex strings
    """

    salt = urandom(32)
    hashed = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed.hex(), salt.hex()
