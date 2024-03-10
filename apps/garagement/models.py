from django.db import models
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.forms import ValidationError

from apps.authentication.models import CustomUser
from apps.garagement.enums import GarageStatus


class Address(models.Model):
    # Es el número asignado a un edificio a lo largo de una calle o una vía
    street_number = models.CharField(max_length=8, blank=False, null=False)
    # Contiene el número del piso en caso de ser necesario
    unit_number = models.CharField(max_length=8, blank=True, null=True)
    # Contiene la parte principal de la dirección, como el nombre de la calle o de la vía
    address_line = models.TextField(blank=False, null=False)
    city = models.CharField(max_length=256, blank=False, null=False)
    region = models.CharField(max_length=256, blank=False, null=False)
    country = CountryField(blank_label='(seleccionar país)', blank=False, null=False)
    postal_code = models.CharField(max_length=16, blank=False, null=False)

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['region']),
            models.Index(fields=['postal_code'])
        ]

    def __str__(self):
        parts = [self.street_number, self.address_line, self.city, self.region, self.country.name]
        return ", ".join(filter(None, parts))

class Garage(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    description = models.TextField(max_length=1024, blank=False, null=False)
    height = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    length = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(decimal_places=2, max_digits=8, blank=False, null=False, validators=[MinValueValidator(0)], help_text='Ingresa un valor positivo')  
    creation_date = models.DateField(auto_now_add=True, blank=False, null=False)
    modification_date = models.DateField(auto_now=True, blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=False, null=False)


    @property
    def average_rating(self):
        return self.comments.aggregate(models.Avg('rating'))['rating__avg']

    class Meta:
        verbose_name = "Garaje"
        verbose_name_plural = "Garajes"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['owner']),
        ]

    def clean(self):
        super().clean()
        if self.price < 0:
            raise ValidationError('El precio no puede ser negativo')

    def __str__(self):
        return f"{self.name} - {str(self.address)}"
    
class Image(models.Model):
    image = models.ImageField(
        upload_to="images/",
        blank=False,
        null=False,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])
        ]
    )
    alt = models.CharField(max_length=256, blank=False, null=False)
    publication_date = models.DateField(auto_now=True, blank=False, null=False)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, blank=False, null=False) 

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"
        unique_together = ('garage','alt')

    def __str__(self):
        return f"{self.garage} - {self.alt}"  
    
class Availability(models.Model):
    start_date=models.DateTimeField(blank=False, null=False)
    end_date=models.DateTimeField(blank=False, null=False)
    status = models.CharField(max_length=16, choices=GarageStatus.choices(), default=GarageStatus.AVAILABLE, blank=False, null=False)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, blank=False, null=False) 

    class Meta:
        verbose_name = "Disponibilidad"
        verbose_name_plural = "Disponibilidades"
        
    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('La fecha de inicio no puede ser mayor que la fecha de fin')

    def __str__(self):
        return f"({self.status}) - Garage: {self.garage}"