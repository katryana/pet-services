from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        ordering = ("username",)

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class Dog(models.Model):
    name = models.CharField(max_length=63)
    age = models.IntegerField()
    breed = models.CharField(max_length=63)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    def __str__(self) -> str:
        return f"{self.breed}: {self.name}, {self.age}"


class Service(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return self.name


class VetClinic(models.Model):
    name = models.CharField(max_length=63)
    city = models.CharField(max_length=63)
    services = models.ManyToManyField(Service, related_name="vet_clinics")

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name}"


class Doctor(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    services = models.ManyToManyField(Service, related_name="doctors")
    vet_clinics = models.ForeignKey(
        VetClinic, on_delete=models.CASCADE, related_name="doctors"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
