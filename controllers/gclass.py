from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from models.learning_env_class import GoogleClass
from models.credentials import GoogleCredentials
from typing import Callable, Dict, List
from .learning_env import LearningEnv

class GoogleClassroomClient(LearningEnv):
    def __init__(self, credentials: Dict, on_token_refresh: Callable[[GoogleCredentials], None]):
        # Create Google Credentials object from the given credentials
        self._credentials = credentials
        creds = Credentials.from_authorized_user_info(credentials)

        # Check if credentials are valid
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

                # Update credentials
                self._credentials = GoogleCredentials(
                    email=self._credentials.email,
                    token=creds.token,
                    refresh_token=creds.refresh_token,
                    token_uri=creds.token_uri,
                    client_id=creds.client_id,
                    client_secret=creds.client_secret,
                    scopes=creds.scopes,
                    id_token=creds.id_token,
                    expiry=f'{creds.expiry.isoformat()}Z'
                )
                on_token_refresh(self._credentials)
            else:
                raise Exception('Invalid credentials')

        # Create Google Classroom API service
        self.service = build('classroom', 'v1', credentials=creds)
    
    @property
    def credentials(self) -> GoogleCredentials:
        return self._credentials
    
    def get_classes(self) -> List[GoogleClass]:
        results = self.service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])
        classes = []
        
        for course in courses:
            classes.append(GoogleClass(
                class_id=int(course['id']),
                name=course['name'],
                description=course['descriptionHeading'],
                url=course['alternateLink']
            ))
        return classes
    
    def get_deadlines(self) -> List[str]:
        pass
        