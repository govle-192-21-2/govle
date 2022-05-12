from dataclasses import dataclass
from datetime import datetime
from json import JSONEncoder
from tkinter import E
from typing import Dict, List


@dataclass
class Deadline:
    """
    Dataclass for a deadline.
    """

    # Name of the assignment
    name: str

    # Deadline date, in Unix timestamp format
    timestamp: int

    # Course to which the deadline belongs
    course: str

    # Course link
    course_url: str

    # Platform that the course is on
    platform: str

    # URL to the assignment, if any
    url: str = None


class DeadlineEnc(JSONEncoder):
    """
    JSONEncoder for Deadline objects.
    """

    def default(self, o):
        if isinstance(o, Deadline):
            return {
                'name': o.name,
                'timestamp': o.timestamp,
                'course': o.course,
                'course_id': o.course_id,
                'platform': o.platform,
                'url': o.url
            }
        return JSONEncoder.default(self, o)


def sort_deadlines(raw_deadlines: List[Deadline]) -> Dict[str, any]:
    # Sort deadlines by date, and then by course
    deadlines = {}
    for deadline in raw_deadlines:
        # Parse date from Unix timestamp
        if deadline.timestamp != 0:
            parsed_date = datetime.utcfromtimestamp(deadline.timestamp)
            parsed_date_str = parsed_date.strftime('%Y-%m-%d')
        else:
            parsed_date_str = '0'

        # Add date to dict if not existing
        if not parsed_date_str in deadlines.keys():
            deadlines[parsed_date_str] = {}
        
        # Add course to dict under date if not existing
        if not deadline.course in deadlines[parsed_date_str].keys():
            deadlines[parsed_date_str][deadline.course] = {
                'name': deadline.course,
                'url': deadline.course_url,
                'deadlines': []
            }
        
        # Add deadline to dict under course
        deadlines[parsed_date_str][deadline.course]['deadlines'].append({
            'name': deadline.name,
            'url': deadline.url,
            'timestamp': deadline.timestamp
        })
    
    # Sort deadlines per course by timestamp
    for date in deadlines.keys():
        for course in deadlines[date].keys():
            deadlines[date][course]['deadlines'].sort(key=lambda x: x['timestamp'])
    
    return deadlines
