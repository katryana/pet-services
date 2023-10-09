from django.test import TestCase

from training_centers.models import Service, TrainingCenter


class ModelsTests(TestCase):
    def test_service_str(self):
        service = Service.objects.create(
            name="Vet care",
            price=120.00
        )
        self.assertEquals(
            str(service),
            service.name
        )

    def test_training_center_str(self):
        training_center = TrainingCenter.objects.create(
            name="test",
            city="test"
        )
        self.assertEquals(
            str(training_center),
            training_center.name
        )

