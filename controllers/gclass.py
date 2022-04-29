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
        creds = Credentials.from_authorized_user_info(credentials)

        # Check if credentials are valid
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

                # Update credentials
                on_token_refresh(GoogleCredentials(
                    email=credentials['email'],
                    token=creds.token,
                    refresh_token=creds.refresh_token,
                    token_uri=creds.token_uri,
                    client_id=creds.client_id,
                    client_secret=creds.client_secret,
                    scopes=creds.scopes,
                    id_token=creds.id_token,
                    expiry=f'{creds.expiry.isoformat()}Z',
                    user_id=credentials['user_id']
                ))
            else:
                raise Exception('Invalid credentials')

        # Create Google Classroom API service
        self.service = build('classroom', 'v1', credentials=creds)
    
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
        my_classes = self.get_classes()
        deadlines_list = []

        for my_class in my_classes:
            class_id = str(my_class.class_id)

            coursework_result = self.service.courses().courseWork().list(courseId=class_id).execute()
            coursework = coursework_result.get('courseWork', [])
            
            if coursework != []:
                deadlines_list.append(coursework)
        
        return deadlines_list