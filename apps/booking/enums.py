from enum import Enum

class ClaimStatus(Enum):

    PENDING = 'Pendiente'
    RESOLVED = 'Resuelta'
    REJECTED = 'Rechazada'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class BookingStatus(Enum):

    PENDING = 'Pendiente'
    CONFIRMED = 'Confirmada'
    CANCELLED = 'Cancelada'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class PaymentMethod(Enum):

    CASH = 'Efectivo'
    CARD = 'CARD'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)