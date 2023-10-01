from django.shortcuts import render

from training_centers.models import TrainingCenter, Specialist, Service


def index(request):
    """View function for the home page of the site."""

    num_vet_clinics = TrainingCenter.objects.count()
    num_services = Service.objects.count()
    num_Specialists = Specialist.objects.count()

    context = {
        "num_vet_clinics": num_vet_clinics,
        "num_services": num_services,
        "num_Specialists": num_Specialists,
    }

    return render(request, "training_centers/index.html", context=context)
