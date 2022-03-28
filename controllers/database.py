from dataclasses import asdict
from firebase_admin.db import Reference
from models.credentials import GoogleCredentials, MoodleCredentials
from models.profile import Profile
from typing import Dict, Optional


def _reconstruct_user_from_db(user_data: Dict) -> Profile:
    # Reconstruct credentials dataclasses
    google_accounts = []
    if 'google_accounts' in user_data:
        google_accounts = [GoogleCredentials(**account) for account in user_data['google_accounts']]
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

    def update_user_google_creds(self, user_id: str, creds: GoogleCredentials):
        """
        Updates a user's Google credentials.

        :param user_id: User ID (string)
        :param creds: GoogleCredentials instance
        """
        # Don't do anything if user does not exist
        user = self.lookup_user_by_id(user_id)
        if not user:
            raise ValueError(f'User {user_id} does not exist')

        # Check if the user has an account already linked
        # User objects in DB are always created with a single GoogleCredentials instance
        # with empty fields, so it suffices to check whether len(_accounts) == 1
        # and accounts[0].token == ''.
        accounts = user.google_accounts
        if not accounts or len(accounts) == 0 or (len(accounts) == 1 and accounts[0].token == ''):
            # Replace the empty account with the new one
            self.root.child(f'users/{user_id}/google_accounts').set([asdict(creds)])
        else:
            # Add the new account to the existing list
            self.root.child(f'users/{user_id}/google_accounts').push(asdict(creds))
