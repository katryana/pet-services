from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from training_centers import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("training_centers.urls", namespace="training-centers")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.UserCreateView.as_view(), name="register"),
    path("", include("theme_pixel.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "training_centers.views.handling_404"
handler403 = "training_centers.views.handling_403"
