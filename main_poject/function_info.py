from dataclasses import dataclass
from typing import Any, List

@dataclass
class function_info:
    """
    Data class to store information about a function.
    """

    name: str               # Name of the function
    args: List[str]         # List of arguments
    return_value: Any       # Return value of the function
