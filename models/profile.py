from abc import ABC
from dataclasses import dataclass
from typing import List
from models.credentials import GoogleCredentials, MoodleCredentials


@dataclass
class Profile(ABC):
    # User name
    name: str

    # User e-mail address
    email: str

    # User profile picture URL
    picture: str

    # Linked Google accounts
    google_accounts: List[GoogleCredentials]

    # Linked Moodle account
    moodle_account: MoodleCredentials
