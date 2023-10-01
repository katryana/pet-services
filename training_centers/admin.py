from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Dog, TrainingCenter, Specialist, Service, Breed


admin.site.unregister(Group)
admin.site.register(User)


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
