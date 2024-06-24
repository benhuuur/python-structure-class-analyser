from dataclasses import dataclass
from typing import Any, List

from data_class.JSON_serializer import JSON_serializable


@dataclass
class function_info():
    """
    Data class to store information about a function.
    """

    name: str
    args: List[str]
    return_value: Any
