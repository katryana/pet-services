from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from training_centers.models import Appointment, Breed, Dog


class AppointmentCreationForm(forms.ModelForm):
    visit_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        initial="visit_date"
    )
    visit_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time", "step": 3600000}),
        initial="visit_time"
    )

    class Meta:
        model = Appointment
        fields = (
            "training_center",
            "service",
            "specialist",
            "visit_date",
            "visit_time"
        )

    def clean(self):
        cleaned_data = super().clean()
        visit_date = cleaned_data.get("visit_date")
        visit_time = cleaned_data.get("visit_time")

        if visit_date and visit_time:
            visit_datetime = datetime.combine(visit_date, visit_time)

            if visit_datetime <= datetime.now():
                raise forms.ValidationError(
                    "Appointment must be scheduled in the future."
                )

            if visit_datetime.year > datetime.now().year + 1:
                raise forms.ValidationError(
                    "Appointment must be scheduled in the current or following year."
                )

        if visit_time:
            if visit_time.hour < 8 or visit_time.hour > 19 or visit_time.minute != 0:
                raise forms.ValidationError(
                    "Appointment time must be between 8:00 and 19:00 "
                    "and have 00 minutes."
                )

        return cleaned_data


class BreedCreationForm(forms.ModelForm):
    class Meta:
        model = Breed
        fields = "__all__"


class DogCreationForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ("name", "age", "breed", )


class CustomUserCreationForm(UserCreationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input hide-remember-me"}
        )
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "email",
        )


class CustomUserUpdateForm(forms.ModelForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "profile_image",
            "first_name",
            "last_name",
            "email",
            "bio",
        )


class SearchForm(forms.Form):
    search_field = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search"
            }
        )
    )
