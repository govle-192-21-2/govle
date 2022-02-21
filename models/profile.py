from dataclasses import dataclass
from flask_login import UserMixin
from hashlib import pbkdf2_hmac
from models.credentials import GoogleCredentials, MoodleCredentials
from typing import List

@dataclass
class Profile(UserMixin):
    # User ID (for LoginManager)
    user_id: str

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

    def verify_password(self, password: str) -> bool:
        """
        Checks if a given password matches a class instance's salted and hashed password.

        :param password: Password to be checked
        :return: True if password matches, False otherwise
        """

        salt_bytes = bytes.fromhex(self.salt)
        password_hashed = pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000)
        return password_hashed.hex() == self.hashed_password
