from dataclasses import dataclass
from flask_login import UserMixin
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

