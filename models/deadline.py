from dataclasses import dataclass
from json import JSONEncoder


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

    # Course ID
    course_id: int

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
