from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Dog, VetClinic, Doctor, Service


admin.site.register(User)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_filter = ["owner", "breed", ]
    search_fields = ["owner", ]


@admin.register(VetClinic)
class VetClinicAdmin(admin.ModelAdmin):
    list_filter = ["city", ]
    search_fields = ["name", ]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_filter = ["services", "vet_clinics", ]
    search_fields = ["first_name", "last_name", ]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    list_display = ["name", "price"]

