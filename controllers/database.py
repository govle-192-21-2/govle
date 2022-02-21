from firebase_admin.db import Reference
from models.credentials import GoogleCredentials, MoodleCredentials
from models.profile import Profile

def load_user(ref: Reference, user_id: str) -> Profile:
    """
    Loads a user from the database and returns a Profile instance.
    For use with Flask-Login.

    :param ref: Firebase DB reference object
    :param user_id: User ID (string)
    :return: Profile instance
    """
    loaded_user = ref.child(user_id).get()

    # Reconstruct credentials dataclasses
    google_accounts = [GoogleCredentials(**account) for account in loaded_user['google_accounts']]
    moodle_account = MoodleCredentials(**loaded_user['moodle_account'])

    return Profile(
        user_id=user_id,
        name=loaded_user['name'],
        email=loaded_user['email'],
        hashed_password=loaded_user['hashed_password'],
        salt=loaded_user['salt'],
        picture=loaded_user['picture'],
        google_accounts=google_accounts,
        moodle_account=moodle_account
    )
