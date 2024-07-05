from dataclasses import dataclass
from typing import List

from data_class.attribute_information import AttributeInformation
from data_class.function_information import FunctionInformation
from file_operations import SerializableToDict


@dataclass
class ClassInformation(SerializableToDict):
    """
    Data class to store information about a class.

    Attributes:
    - name (str): The name of the class.
    - inheritance (List[str]): List of inherited class names.
    - attributes (List[AttributeInfo]): List of AttributeInfo objects representing attributes.
    - methods (List[FunctionInfo]): List of FunctionInfo objects representing methods.
    """

    name: str
    inheritance: List[str]
    attributes: List[AttributeInformation]
    methods: List[FunctionInformation]

    def to_dict(self) -> dict:
        """
        Converts the ClassInfo object into a dictionary representation suitable for JSON serialization.

        Returns:
        - dict: A dictionary containing the class information.
            {
                "class_name": str,          # The name of the class.
                "inheritance": List[str],   # List of inherited class names.
                "attributes": List[dict],   # List of dictionaries representing attributes (AttributeInfo objects).
                "methods": List[dict]       # List of dictionaries representing methods (FunctionInfo objects).
            }
        """
        return {
            "class_name": self.name,
            "inheritance": self.inheritance,
            "attributes": [attribute.__dict__ for attribute in self.attributes],
            "methods": [method.__dict__ for method in self.methods],
        }
