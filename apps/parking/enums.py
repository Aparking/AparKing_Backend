from enum import Enum

class Size(Enum):

    BERLINA = 'Berlina'
    COMPACTO = 'Compacto'
    SEDAN = 'Sedan'
    FURGONETA = 'Furgoneta'
    SUV = 'SUV'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)