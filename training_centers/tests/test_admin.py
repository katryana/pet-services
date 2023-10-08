from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="user",
            first_name="Mary",
            last_name="Smith",
            password="test123user",
            profile_image=""
        )

    def test_user_attributes_listed(self):
        """
        Test that user's profile image is
        in list_display on user admin page
        """
        url = reverse("admin:training_centers_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.profile_image)

    def test_user_detail_attributes_listed(self):
        """
        Test that user's profile image is on user detail admin page
        """
        url = reverse("admin:training_centers_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertContains(res, self.user.profile_image)
