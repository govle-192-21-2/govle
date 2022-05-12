from dataclasses import dataclass


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
