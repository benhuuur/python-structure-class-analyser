class data_class:
    def __init__(self, name, heritage, attribute, methods, identation_level=0):
        self._name = name
        self._heritage = heritage
        self._attribute = attribute
        self._methods = methods
        self._identation_level = identation_level
    
    def get_name(self):
        return self._name
    
    def get_heritage(self):
        return self._heritage
    
    def get_identation_level(self):
        return self._identation_level
    
    def __str__(self):
        methods_str = ", ".join(str(method) for method in self._methods)
        return f"Name: {self._name}, Heritage: {self._heritage}, Methods: [{methods_str}], Attribute: {self._attribute}"

    