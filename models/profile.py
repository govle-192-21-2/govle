from dataclasses import dataclass
from flask_login import UserMixin
from hashlib import pbkdf2_hmac
from models.credentials import GoogleCredentials, MoodleCredentials
from os import urandom
from typing import List, Tuple

@dataclass
class Profile(UserMixin):
    # User name
    name: str

    # User e-mail address
    email: str

    # User password, salted and hashed
    hashed_password: str

    # User password salt
    salt: str

    # User profile picture URL
    picture: str

    # Linked Google accounts
    google_accounts: List[GoogleCredentials]

    # Linked Moodle account
    moodle_account: MoodleCredentials


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


def check_password(password: str, hashed: str, salt: str) -> bool:
    """
    Checks if a given password matches a given salted and hashed password.

    :param password: Password to be checked
    :param hashed: Hashed password (byte array encoded as hex string)
    :param salt: Salt (byte array encoded as hex string)
    :return: True if password matches, False otherwise
    """

    salt_bytes = bytes.fromhex(salt)
    password_hashed = pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000)
    return password_hashed.hex() == hashed
