from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import LoginView, LogoutView, RegisterView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    # (anyone can access)
    path("users/register/", RegisterView.as_view(), name="user-register"),
    path("users/login/", LoginView.as_view(), name="user-login"),


    path("users/logout/", LogoutView.as_view(), name="user-logout"),

    # CRUD endpoints (must be logged in)
    path("", include(router.urls)),
]
