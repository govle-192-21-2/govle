from abc import ABC
from dataclasses import dataclass
from json import JSONEncoder


@dataclass
class LearningEnvClass(ABC):
    """
    Abstract dataclass for a learning environment class object.
    """
    # Class ID
    class_id: int

    # Class name
    name: str

    # Class description
    description: str

    # Class URL (link to external learning environment)
    url: str


class GoogleClass(LearningEnvClass):
    """
    Abstract dataclass for a class hosted on Google Classroom.
    """
    pass


class MoodleClass(LearningEnvClass):
    """
    Abstract dataclass for a class hosted on Moodle.
    """
    completion_status: float


class LearningEnvClassEnc(JSONEncoder):
    """
    JSON encoder for LearningEnvClass
    """
    def default(self, o):
        if isinstance(o, LearningEnvClass):
            return {
                'class_id': o.class_id,
                'name': o.name,
                'description': o.description,
                'url': o.url
            }
        else:
            return super().default(o)
