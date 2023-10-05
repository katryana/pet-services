from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/profile/")

    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return self.username


class Appointment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    training_center = models.ForeignKey(
        "TrainingCenter",
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    specialist = models.ForeignKey(
        "Specialist",
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    visit_date = models.DateField()
    visit_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["specialist", "visit_date", "visit_time"],
                name="unique_appointment",
                violation_error_message="The meeting with this specialist on this time has been already appointed."
            ),
        ]
        ordering = ("-visit_date", "-visit_time")

    def clean(self):
        super().clean()

        if self.service not in self.training_center.services.all():
            raise ValidationError("The selected service is not provided in the chosen training center.")

        if self.specialist.training_centers != self.training_center:
            raise ValidationError("The chosen specialist does not work in the selected training center.")

        if self.service not in self.specialist.services.all():
            raise ValidationError("The chosen specialist does not provide this service.")

    def __str__(self) -> str:
        return f"{self.user} {self.visit_date.strftime('%d-%m-%Y %H:%M')}"


class Breed(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255)
    breed_image = models.ImageField(null=True, blank=True, upload_to="images/breeds/")

    class Meta:
        ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Dog(models.Model):
    name = models.CharField(max_length=63)
    age = models.PositiveIntegerField()
    breed = models.ForeignKey(
        Breed,
        on_delete=models.PROTECT,
        related_name="dogs"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dogs"
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name}, {self.breed}"


def validate_positive_price(value):
    if value <= 0:
        raise ValidationError("Price must be greater than zero.")


class Service(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[validate_positive_price]
    )
    breeds = models.ManyToManyField(Breed, related_name="services")

    class Meta:
        ordering = ("price",)

    def __str__(self) -> str:
        return self.name


class TrainingCenter(models.Model):
    name = models.CharField(max_length=63)
    city = models.CharField(max_length=63)
    services = models.ManyToManyField(Service, related_name="training_centers")

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Specialist(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format:"
                        " '+123456789'. Up to 15 digits allowed."
            )
        ]
    )
    email_address = models.EmailField()
    years_of_experience = models.PositiveIntegerField()
    services = models.ManyToManyField(Service, related_name="specialists")
    training_centers = models.ForeignKey(
        TrainingCenter, on_delete=models.CASCADE, related_name="specialists"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
