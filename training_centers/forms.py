from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateTimeInput

from training_centers.models import Appointment


class AppointmentCreationForm(forms.ModelForm):
    visit_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%d-%m-%Y %H:%M"),
        input_formats=["%d-%m-%Y %H:%M"],
    )

    class Meta:
        model = Appointment
        fields = (
            "service", "specialist", "visit_date",
        )

    def clean_date_time(self):
        date_time = self.cleaned_data["visit_date"]

        if (date_time.hour < 8 or date_time.hour > 19) or date_time.minute != 0:
            raise ValidationError(
                "Working hours must be in 8:00 to 19:00."
                "Minutes of an appointment must be equal to 0."
            )

        return date_time
