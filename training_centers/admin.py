from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import (
    User,
    Dog,
    TrainingCenter,
    Specialist,
    Service,
    Breed,
    Appointment
)

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("bio", "profile_image", )}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "profile_image",
                    )
                },
            ),
        )
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ["visit_date", ]
    list_filter = ["training_center", "specialist", "service", ]


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    search_fields = ["name", ]


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_filter = ["owner", "breed", ]
    search_fields = ["name", ]
    list_display = ["name", "breed", "owner", ]


@admin.register(TrainingCenter)
class TrainingCenterAdmin(admin.ModelAdmin):
    list_filter = ["city", ]
    search_fields = ["name", ]


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_filter = ["training_centers", "services", ]
    search_fields = ["first_name", "last_name", ]
    list_display = ["first_name", "last_name", "training_centers", "phone_number"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_filter = ["breeds", ]
    list_display = ["name", "price"]
