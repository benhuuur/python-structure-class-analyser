from dataclasses import dataclass
from typing import Any, List

from function_info import function_info

@dataclass
class assignments_info:
    """
    Data class to store information about a class.
    """

    name: str
    data_type: Any
    encapsulation: str
