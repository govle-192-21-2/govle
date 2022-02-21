from dataclasses import dataclass, field
from models.credentials import GoogleCredentials, MoodleCredentials
from typing import Dict, List, Union

@dataclass
class Profile():
    # User ID (for LoginManager)
    user_id: str

    # User name
    name: str

    # User e-mail address
    email: str

    # Linked Moodle account
    moodle_account: MoodleCredentials

    # Linked Google accounts
    google_accounts: List[GoogleCredentials]

    # User profile picture
    picture: str = field(default='')

    def __post_init__(self):
        """
        Initializes a Profile instance.
        """
        self._is_authenticated = True
        self._is_active = True
        self._is_anonymous = False
    
    @property
    def is_authenticated(self) -> bool:
        """
        Returns whether the user is authenticated or not. This is used by Flask-Login.

        :return: True if authenticated, False otherwise
        """
        return self._is_authenticated
    
    @property
    def is_active(self) -> bool:
        """
        Returns whether the user is active or not. This is used by Flask-Login.

        :return: True if active, False otherwise
        """
        return self._is_active
    
    @property
    def is_anonymous(self) -> bool:
        """
        Returns whether the user is anonymous or not. This is used by Flask-Login.

        :return: True if anonymous, False otherwise
        """
        return self._is_anonymous
    
    def get_id(self) -> str:
        """
        Returns the user ID. This is used by Flask-Login.

        :return: User ID
        """
        return self.user_id


def create_from_google_jwt(jwt_info: Dict[str, Union[str, int, bool]]) -> Profile:
    return Profile(
        user_id=jwt_info['sub'],
        name=jwt_info['name'],
        email=jwt_info['email'],
        picture=jwt_info['picture'],
        moodle_account=MoodleCredentials(),
        google_accounts=[GoogleCredentials()]
    )
