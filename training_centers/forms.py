from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from training_centers.models import Appointment, TrainingCenter, Specialist, Service


class AppointmentCreationForm(forms.ModelForm):
    visit_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%d-%m-%Y %H:%M"),
        input_formats=["%d-%m-%Y %H:%M"],
    )

    class Meta:
        model = Appointment
        fields = (
            "training_center",
            "service",
            "specialist",
            "visit_date",
        )


    def clean_visit_date(self):
        date_time = self.cleaned_data["visit_date"]
        current_datetime = datetime.now()

        if date_time.replace(tzinfo=None) <= current_datetime.replace(tzinfo=None):
            raise ValidationError("Appointment date and time must be in the future.")

        if not (8 <= date_time.hour <= 19) or date_time.minute != 0:
            raise ValidationError(
                "Working hours must be in 8:00 to 19:00."
                " Minutes of an appointment must be equal to 00."
            )

        return date_time


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
