from dataclasses import dataclass
from typing import List

from JSON_serializer import JSON_serializable
from data_class.assignments_info import assignments_info
from data_class.function_info import function_info


@dataclass
class class_info(JSON_serializable):
    """
    Data class to store information about a class.
    """

    name: str
    heritage: List[str]
    functions: List[function_info]
    assignments: List[assignments_info]

    def to_dict(self):
        return {
            "name": self.name,
            "heritage": self.heritage,
            "functions": [function.__dict__ for function in self.functions],
            "assignments": [assignment.__dict__ for assignment in self.assignments]
        }
