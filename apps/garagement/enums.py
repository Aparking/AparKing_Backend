from enum import Enum

class GarageStatus(Enum):

    AVAILABLE = 'Disponible'
    NOTAVAILABLE = 'No disponible'
    RESERVED = 'Reservada'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)