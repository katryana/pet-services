from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import AppointmentCreationForm, SearchForm, CustomUserCreationForm, CustomUserUpdateForm, BreedCreationForm, \
    DogCreationForm
from .models import TrainingCenter, Specialist, Service, Appointment, Dog, Breed


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


def index(request):
    """View function for the home page of the site."""

    num_training_centers = TrainingCenter.objects.count()
    num_services = Service.objects.count()
    num_specialists = Specialist.objects.count()
    num_users = get_user_model().objects.count()

    context = {
        "num_training_centers": num_training_centers,
        "num_services": num_services,
        "num_specialists": num_specialists,
        "num_users": num_users
    }

    return render(request, "training_centers/index.html", context=context)


def handling_404(request, exception=None):
    return render(request, "404.html", status=404)


def handling_403(request, exception=None):
    return render(request, "403.html", status=403)


class UserCreateView(generic.CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"

    def get_success_url(self):
        auth_user = self.object
        remember_me = self.request.POST.get("remember_me")
        if remember_me:
            login(self.request, auth_user)
        else:
            pass

        success_url = reverse_lazy("training-centers:index")
        return success_url


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


class BreedListView(generic.ListView):
    model = Breed
    paginate_by = 3
    queryset = Breed.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get("search_field", "")
        context["search_form"] = SearchForm(
            initial={"search_field": search_input}
        )
        return context


class BreedCreateView(SuperUserRequiredMixin, generic.CreateView):
    model = Breed
    success_url = reverse_lazy("training-centers:breed-list")
    form_class = BreedCreationForm


class BreedUpdateView(SuperUserRequiredMixin, generic.UpdateView):
    form_class = BreedCreationForm
    success_url = reverse_lazy("training-centers:breed-list")


class BreedDeleteView(SuperUserRequiredMixin, generic.DeleteView):
    model = Breed
    success_url = reverse_lazy("training-centers:breed-list")


class DogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dog
    success_url = reverse_lazy("training-centers:dog-list")
    form_class = DogCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DogUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = DogCreationForm
    success_url = reverse_lazy("training-centers:dog-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        appointment = super().get_object(queryset)

        required_id = appointment.user.id
        user_id = self.request.user.id

        if user_id != required_id:
            raise Http404("You don't have permission to access this page")

        return appointment


class DogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dog
    success_url = reverse_lazy("training-centers:dog-list")

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(user__id=user.id)


class SpecialistListView(generic.ListView):
    model = Specialist
    paginate_by = 3
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


class ProfileDetailView(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomUserUpdateForm
    template_name = "training_centers/profile_detail.html"
    context_object_name = "user"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        user_id = self.object.id

        success_url = reverse_lazy("training-centers:profile-detail", args=[user_id])
        return success_url

    def get_queryset(self):
        user = self.request.user
        return get_user_model().objects.filter(id=user.id)


class SpecialistDetailView(generic.DetailView):
    model = Specialist


class DogListView(LoginRequiredMixin, generic.ListView):
    model = Dog

    def get_queryset(self):
        user = self.request.user
        return Dog.objects.filter(owner_id=user.id)


class AppointmentListView(LoginRequiredMixin, generic.ListView):
    model = Appointment
    paginate_by = 1

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


class AppointmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = AppointmentCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        appointment_id = self.object.id

        success_url = reverse_lazy("training-centers:appointment-detail", args=[appointment_id])
        return success_url

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
