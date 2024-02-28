from enum import Enum

class Gender(Enum):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)