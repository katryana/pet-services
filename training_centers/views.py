from django.shortcuts import render
from django.views import generic

from training_centers.models import TrainingCenter, Specialist, Service


def index(request):
    """View function for the home page of the site."""

    num_training_centers = TrainingCenter.objects.count()
    num_services = Service.objects.count()
    num_specialists = Specialist.objects.count()

    context = {
        "num_training_centers": num_training_centers,
        "num_services": num_services,
        "num_specialists": num_specialists,
    }

    return render(request, "training_centers/index.html", context=context)


class ServiceListView(generic.ListView):
    model = Service
    context_object_name = "service_list"
    template_name = "training_centers/service_list.html"
    paginate_by = 10
    queryset = Service.objects.prefetch_related("breeds")


class TrainingCenterListView(generic.ListView):
    model = TrainingCenter
    context_object_name = "training_center_list"
    template_name = "training_centers/training_center_list.html"
    paginate_by = 10
    queryset = TrainingCenter.objects.prefetch_related("services")


class SpecialistListView(generic.ListView):
    model = Specialist
    paginate_by = 7
    specialists = Specialist.objects.select_related("training_centers")
    queryset = specialists.prefetch_related("services")
