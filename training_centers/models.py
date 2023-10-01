from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class Breed(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self) -> str:
        return self.name


class Dog(models.Model):
    name = models.CharField(max_length=63)
    age = models.IntegerField()
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
        return f"{self.name}, owner: {self.owner}"


class Service(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
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
        return f"{self.name}"


class Specialist(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    services = models.ManyToManyField(Service, related_name="specialists")
    training_centers = models.ForeignKey(
        TrainingCenter, on_delete=models.CASCADE, related_name="specialists"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
