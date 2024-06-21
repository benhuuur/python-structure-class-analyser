from dataclasses import dataclass
from typing import Any, List

from function_info import function_info

@dataclass
class class_info:
    """
    Data class to store information about a class.
    """

    name: str
    heritage: List[str]
    functions: List[function_info]
    assignments: List[str]
