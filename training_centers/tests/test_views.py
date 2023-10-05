from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from training_centers.models import TrainingCenter, Specialist, Service, Appointment, Dog, Breed


class TrainingCenterViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test"
        )

        self.training_center = TrainingCenter.objects.create(
            name="Test Training Center",
            city="Test City"
        )

        self.specialist = Specialist.objects.create(
            first_name="Test",
            last_name="Specialist",
            phone_number="1234567890",
            email_address="test@example.com",
            years_of_experience=5,
            training_centers=self.training_center
        )

        self.service = Service.objects.create(
            name="Test Service",
            description="Test Service Description",
            price=10.0
        )

        self.appointment = Appointment.objects.create(
            user=self.user,
            training_center=self.training_center,
            specialist=self.specialist,
            service=self.service,
            visit_date="2023-12-31",
            visit_time="10:00"
        )

        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse("training-centers:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TrainingCenter.objects.count())

    def test_training_center_list_view(self):
        # Test the training center list view
        response = self.client.get(reverse("training-centers:training-center-list"))
        self.assertEqual(response.status_code, 200)


    def test_training_center_detail_view(self):
        url = reverse("training-centers:training-center-detail", args=[self.training_center.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_specialist_list_view(self):
        response = self.client.get(reverse("training-centers:specialist-list"))
        self.assertEqual(response.status_code, 200)


    def test_specialist_detail_view(self):
        url = reverse("training-centers:specialist-detail", args=[self.specialist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
