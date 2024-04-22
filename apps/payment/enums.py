from enum import Enum

class MemberType(Enum):

    FREE = 'Gratuita'
    NOBLE = 'Noble'
    KING = 'King'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)