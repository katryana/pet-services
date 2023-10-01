from django.urls import path

from .views import (
    index,
    ServiceListView, TrainingCenterListView, SpecialistListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("specialists/", SpecialistListView.as_view(), name="specialist-list"),
    path(
        "training-centers/",
        TrainingCenterListView.as_view(),
        name="training-center-list"
    ),
]

app_name = "training-centers"
