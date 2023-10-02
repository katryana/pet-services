from django.urls import path

from .views import (
    index,
    ServiceListView,
    TrainingCenterListView,
    SpecialistListView,
    TrainingCenterDetailView,
    ServiceDetailView,
    SpecialistDetailView,
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
    path(
        "training-centers/<int:pk>/",
        TrainingCenterDetailView.as_view(),
        name="training-center-detail"
    ),
    path(
        "services/<int:pk>/",
        ServiceDetailView.as_view(),
        name="service-detail"
    ),
    path(
        "specialists/<int:pk>/",
        SpecialistDetailView.as_view(),
        name="specialist-detail"
    ),
]

app_name = "training-centers"
