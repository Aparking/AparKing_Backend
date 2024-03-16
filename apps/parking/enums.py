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
from enum import Enum

class ParkingType(Enum):
    ASSIGNMENT = "ASSIGNMENT"
    FREE = "FREE"
    PRIVATE = "PRIVATE"

class ParkingSize(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class NoticationsSocket(Enum):
    PARKING_DELETED = "notify.parking.deleted"
    PARKING_BOOKED = "notify.parking.booked"
    PARKING_NOTIFIED = "notify.parking.created"