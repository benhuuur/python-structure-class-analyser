class data_function:
    def __init__(self, name, args) -> None:
        self._name = name
        self._args = args
    
    def __str__(self):
        return f"Name: {self._name}, Args: {self._args}"