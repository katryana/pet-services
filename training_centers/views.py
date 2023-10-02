from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from training_centers.forms import AppointmentCreationForm, SearchForm
from training_centers.models import TrainingCenter, Specialist, Service, Appointment


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
    paginate_by = 3
    queryset = Service.objects.prefetch_related("breeds")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("search_field", "")
        context["search_form"] = SearchForm(
            initial={"search_field": name}
        )
        return context

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return Service.objects.filter(
                name__icontains=form.cleaned_data["search_field"]
            )
        return Service.objects.all()


class SpecialistListView(generic.ListView):
    model = Specialist
    paginate_by = 7
    specialists = Specialist.objects.select_related("training_centers")
    queryset = specialists.prefetch_related("services")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get("search_field", "")
        context["search_form"] = SearchForm(
            initial={"search_field": search_input}
        )
        return context

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return Specialist.objects.filter(
                Q(first_name__icontains=form.cleaned_data["search_field"])
                | Q(last_name__icontains=form.cleaned_data["search_field"])
            )
        return Specialist.objects.all()


class TrainingCenterListView(generic.ListView):
    model = TrainingCenter
    context_object_name = "training_center_list"
    template_name = "training_centers/training_center_list.html"
    paginate_by = 3
    queryset = TrainingCenter.objects.prefetch_related("services")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get("search_field", "")
        context["search_form"] = SearchForm(
            initial={"search_field": search_input}
        )
        return context

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return TrainingCenter.objects.filter(
                city__icontains=form.cleaned_data["search_field"]
            )
        return TrainingCenter.objects.all()


class TrainingCenterDetailView(generic.DetailView):
    model = TrainingCenter
    template_name = "training_centers/training_center_detail.html"
    context_object_name = "training_center"


class ServiceDetailView(generic.DetailView):
    model = Service


class SpecialistDetailView(generic.DetailView):
    model = Specialist


class AppointmentListView(LoginRequiredMixin, generic.ListView):
    model = Appointment

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(user__id=user.id)


class AppointmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Appointment
    template_name = "training_centers/appointment_detail.html"
    context_object_name = "appointment"

    def get_object(self, queryset=None):
        appointment = super().get_object(queryset)

        required_id = appointment.user.id
        user_id = self.request.user.id

        if user_id != required_id:
            raise Http404("You don't have permission to access this page")

        return appointment


class AppointmentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Appointment
    success_url = reverse_lazy("training-centers:appointment-list")
    form_class = AppointmentCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    success_url = reverse_lazy("training-centers:appointment-list")
    form_class = AppointmentCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(user__id=user.id)

    def get_initial(self):
        initial = super().get_initial()
        appointment = self.object
        initial["visit_date"] = appointment.visit_date
        return initial


class AppointmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Appointment
    success_url = reverse_lazy("training-centers:appointment-list")

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(user__id=user.id)
