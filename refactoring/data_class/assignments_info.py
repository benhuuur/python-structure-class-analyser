from dataclasses import dataclass
from typing import Any


@dataclass
class assignments_info:
    """
    Data class to store information about a varible assignment.
    """

    name: str
    data_type: str
    encapsulation: str
