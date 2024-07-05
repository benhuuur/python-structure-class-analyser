from dataclasses import dataclass
from typing import Any, List


@dataclass
class FunctionInformation:
    """
    Data class to store information about a function.
    """

    name: str
    args: List[str]
    return_value: Any
