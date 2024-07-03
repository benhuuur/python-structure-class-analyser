from abc import ABC, abstractmethod
import json


class JSON_serializable(ABC):
    @abstractmethod
    def to_dict(self):
        pass


class JSON_serializer:
    @staticmethod
    def save_to_json(filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file)
