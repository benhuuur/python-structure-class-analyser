from dataclasses import dataclass
from typing import List

from JSON.JSON_serializer import JSON_serializable
from data_class.assignments_info import assignments_info
from data_class.function_info import function_info


@dataclass
class class_info(JSON_serializable):
    """
    Data class to store information about a class.
    """

    name: str
    inheritance: List[str]
    methods: List[function_info]
    attributes: List[assignments_info]

    def to_dict(self):
        """
        Converts the class_info object into a dictionary representation suitable for JSON serialization.

        Returns:
            dict: A dictionary containing the class information.
                {
                    "class_name": str,          # The name of the class.
                    "inheritance": List[str],   # List of inherited class names.
                    "attributes": List[dict],   # List of dictionaries representing attributes (assignments_info objects).
                    "methods": List[dict]       # List of dictionaries representing methods (function_info objects).
                }
        """
        return {
            "class_name": self.name,
            "inheritance": self.inheritance,
            "attributes": [assignment.__dict__ for assignment in self.attributes],
            "methods": [function.__dict__ for function in self.methods],
        }
