from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import (
    Dog,
    TrainingCenter,
    Specialist,
    Service,
    Breed,
    Appointment
)

admin.site.unregister(Group)


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = UserAdmin.list_display + ("bio", "profile_image", )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("bio", "profile_image", )}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "bio",
                        "profile_image",
                    )
                },
            ),
        )
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ["visit_date", ]
    list_filter = ["service", "specialist", ]


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    search_fields = ["name", ]


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_filter = ["owner", "breed", ]
    search_fields = ["name", ]


@admin.register(TrainingCenter)
class TrainingCenterAdmin(admin.ModelAdmin):
    list_filter = ["city", ]
    search_fields = ["name", ]


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_filter = ["services", "training_centers", ]
    search_fields = ["first_name", "last_name", ]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
