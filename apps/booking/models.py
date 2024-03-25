from datetime import datetime
import decimal
from django.db import models
from django.forms import ValidationError

from apps.authentication.models import CustomUser
from apps.booking.enums import BookingStatus, ClaimStatus, PaymentMethod
from apps.garagement.models import Availability, Garage

from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class Comment(models.Model):
    title = models.TextField(max_length=64, blank=False, null=False)
    description = models.TextField(max_length=1024)
    publication_date = models.DateField(auto_now_add=True, blank=False, null=False)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, blank=False, null=False, related_name='comments')

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['garage']),
        ]

    def __str__(self):
        return f"{self.garage.name} : {self.title}"


class Claim(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=False, null=False)
    publication_date = models.DateField(auto_now=True, blank=False, null=False)
    status = models.CharField(max_length=16, choices=ClaimStatus.choices(), default=ClaimStatus.PENDING, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, blank=False, null=False)
    

    class Meta:
        verbose_name = "Reclamación"
        verbose_name_plural = "Reclamaciones"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['garage']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.garage.name} : {self.title}"

class Book(models.Model):
    payment_method=models.CharField(max_length=16, choices=PaymentMethod.choices(), blank=False, null=False)
    status = models.CharField(max_length=16, choices=BookingStatus.choices(), default=BookingStatus.PENDING, blank=False, null=False)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    availability=models.ForeignKey(Availability,on_delete=models.CASCADE, blank=False, null=False)
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['availability']),
            models.Index(fields=['status']),
        ]
    
    def calculate_total_price(self):
        days_difference = (self.availability.end_date.date() - self.availability.start_date.date()).days
        return Decimal(days_difference) * Decimal(self.availability.garage.price)

    def __str__(self):
        username = self.user.username if self.user else None
        return f"{username} : {self.availability.garage.name} - {self.availability.start_date} - {self.availability.end_date}"
