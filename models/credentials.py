from dataclasses import dataclass


@dataclass
class GoogleCredentials():
    # User ID
    user_id: str

    # OAuth2 access token
    access_token: str


@dataclass
class MoodleCredentials():
    # Username
    username: str

    # Password
    password: str

    # Moodle server URL
    server: str
