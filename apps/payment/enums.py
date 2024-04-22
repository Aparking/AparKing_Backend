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
    
class MemberId(Enum):

    FREE = 'price_1OzRzqC4xI44aLdHxKkbcfko'
    NOBLE = 'price_1OzduBC4xI44aLdHVfhBk4MT'
    KING = 'price_1OzduRC4xI44aLdHub5MI81D'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)