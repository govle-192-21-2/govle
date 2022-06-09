from dataclasses import asdict
from firebase_admin.db import Reference
from models.credentials import GoogleCredentials, MoodleCredentials
from models.profile import Profile
from typing import Dict, Optional


def _reconstruct_user_from_db(user_data: Dict) -> Profile:
    # Reconstruct credentials dataclasses
    google_accounts = {}
    if 'google_accounts' in user_data:
        google_accounts = user_data['google_accounts']
    moodle_account = MoodleCredentials(**user_data['moodle_account'])

    return Profile(
        user_id=user_data['user_id'],
        name=user_data['name'],
        email=user_data['email'],
        picture=user_data['picture'],
        google_accounts=google_accounts,
        moodle_account=moodle_account
    )


class Database:
    def __init__(self, ref: Reference):
        self.root: Reference = ref
    
    def add_user(self, user: Profile):
        """
        Adds a new user to the database.
        """
        self.root.child(f'users/{user.user_id}').set(asdict(user))
    
    def delete_user(self, user_id: str):
        """
        Deletes a user from the database.

        :param user_id: User ID (string)
        """
        self.root.child(f'users/{user_id}').delete()
    
    def delete_user_google_creds(self, user_id: str, google_account_id: str):
        """
        Deletes a user's Google credentials.

        :param user_id: User ID (string)
        """
        # Don't do anything if user does not exist
        user = self.lookup_user_by_id(user_id)
        if not user:
            raise ValueError(f'User {user_id} does not exist')

        # Delete credentials under corresponding user ID and Google Account ID
        self.root.child(f'users/{user_id}/google_accounts/{google_account_id}').delete()
    
    def delete_user_moodle_creds(self, user_id: str):
        """
        Deletes a user's Moodle credentials.

        :param user_id: User ID (string)
        """
        # Don't do anything if user does not exist
        user = self.lookup_user_by_id(user_id)
        if not user:
            raise ValueError(f'User {user_id} does not exist')

        # Delete credentials under corresponding user ID
        self.root.child(f'users/{user_id}/moodle_account').set({'password': ''})
    
    def lookup_user_by_email(self, email: str) -> Optional[Profile]:
        """
        Looks up a user by email and returns a Profile instance.

        :param email: User email
        :return: User ID string
        """
        users = self.root.child('users').get()
        if not users:
            return None

        for _, user in users.items():
            if user['email'] == email:
                return _reconstruct_user_from_db(user)
        return None

    def lookup_user_by_id(self, user_id: str) -> Optional[Profile]:
        """
        Loads a user from the database and returns a Profile instance.
        For use with Flask-Login.

        :param ref: Firebase DB reference object
        :param user_id: User ID (string)
        :return: Profile instance
        """
        loaded_user = self.root.child(f'users/{user_id}').get()
        if loaded_user:
            return _reconstruct_user_from_db(loaded_user)
        return None

    def update_user_google_creds(self, user_id: str, cred_id: str, creds: GoogleCredentials):
        """
        Updates a user's Google credentials.

        :param user_id: User ID (string)
        :param creds: GoogleCredentials instance
        """
        # Don't do anything if user does not exist
        user = self.lookup_user_by_id(user_id)
        if not user:
            raise ValueError(f'User {user_id} does not exist')

        # Save credentials under corresponding user ID
        self.root.child(f'users/{user_id}/google_accounts/{cred_id}').set(asdict(creds))
    
    def update_user_moodle_creds(self, user_id: str, creds: MoodleCredentials):
        """
        Updates a user's Moodle credentials.

        :param user_id: User ID (string)
        :param creds: MoodleCredentials instance
        """
        # Don't do anything if user does not exist
        user = self.lookup_user_by_id(user_id)
        if not user:
            raise ValueError(f'User {user_id} does not exist')

        # Save credentials under corresponding user ID
        self.root.child(f'users/{user_id}/moodle_account').set(asdict(creds))
