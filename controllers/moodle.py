from models.credentials import MoodleCredentials
from models.deadline import Deadline
from models.learning_env_class import MoodleClass
from typing import Dict, List, Optional
from .learning_env import LearningEnv
import requests


class MoodleClient(LearningEnv):
    def __init__(self, creds: MoodleCredentials):
        self.credentials = creds
        self.user_id = None
    
    def _perform_request(self, func: str, id_required: bool = False, params: Optional[Dict[str, any]] = {}) -> requests.Response:
        # If id_required, request ID if it hasn't been requested yet
        request_params = {
            'wstoken': self.credentials.password,
            'wsfunction': func,
            'moodlewsrestformat': 'json'
        }
        if id_required:
            request_params['userid'] = self._get_user_id()

        # Update params with any additional parameters
        request_params.update(params)
        
        # Create request and send it to the remote server
        return requests.get(f'https://{self.credentials.server}/webservice/rest/server.php', params=request_params)

    def _get_user_id(self) -> int:
        if self.user_id == None:
            # Cache user ID from server response
            response = self._perform_request('core_webservice_get_site_info')
            self.user_id = response.json()['userid']
        
        return self.user_id
    
    def _get_category_name(self, category_id: int) -> str:
        response = self._perform_request(
            'core_course_get_categories',
            params={
                'criteria[0][key]': 'id',
                'criteria[0][value]': category_id
            }
        )
        
        # We should never get more than one matching category per ID,
        # but just in case...
        for category in response.json():
            if category['id'] == category_id:
                return category['name']

    def get_classes(self) -> List[MoodleClass]:
        classes = []

        # Construct MoodleClass instances from server response
        response = self._perform_request('core_enrol_get_users_courses', id_required=True)
        courses = response.json()
        for course in courses:
            classes.append(MoodleClass(
                class_id=course['id'],
                name=course['fullname'],
                completion_status=course['progress'],
                
                # The Moodle API (if you can call it that) does not return the URL to the course,
                # so we just construct it using the course ID.
                url=f'https://{self.credentials.server}/course/view.php?id={course["id"]}',

                # The 'description' in Moodle is actually
                # the name of the category that the course belongs to.
                description=self._get_category_name(course['category'])
            ))

        return classes

    def get_deadlines(self) -> List[Deadline]:
        deadlines = []

        # Get upcoming view from Moodle API
        response = self._perform_request('core_calendar_get_calendar_upcoming_view')
        events = response.json()['events']
        for event in events:
            # All assignments are actionable events, denoted by ['isactionevent'] == True.
            # Filter for those.
            if not event['isactionevent']:
                continue
            
            # Create Deadline instance from event
            deadlines.append(Deadline(
                name=event['name'],
                timestamp=event['timestart'],
                course=event['course']['id'],
                platform=self.credentials.server,
                url=event['url']
            ))

        return deadlines
