from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from training_centers.forms import SearchForm
from training_centers.models import Specialist, TrainingCenter

SPECIALIST_URL = reverse("training-centers:specialist-list")


class TestManufacturerSearchForm(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1",
            password="test1"
        )
        training_center = TrainingCenter.objects.create()
        Specialist.objects.create(
            first_name="John",
            last_name="MaC",
            years_of_experience=5,
            training_centers=training_center
        )
        Specialist.objects.create(
            first_name="Mary",
            last_name="Smith",
            years_of_experience=3,
            training_centers=training_center
        )
        self.client.force_login(self.user)

    def test_search_form(self):
        form_data = {"search_field": "Jo"}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_search_form_search(self):
        form_data = {"search_field": "Ma"}
        res = self.client.get(SPECIALIST_URL, data=form_data)
        self.assertContains(res, "John")
        self.assertContains(res, "Mary")
        form_data = {"search_field": "Jo"}
        res = self.client.get(SPECIALIST_URL, data=form_data)
        self.assertContains(res, "John")
        self.assertNotContains(res, "Mary")
