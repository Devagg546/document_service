from django.urls import path

from user.views import LoginView, LogoutView, RegisterView, UserViewSet

urlpatterns = [
    # Auth
    path("users/register/", RegisterView.as_view(), name="user-register"),
    path("users/login/", LoginView.as_view(), name="user-login"),
    path("users/logout/", LogoutView.as_view(), name="user-logout"),

    # User CRUD — each action gets its own descriptive URL
    path("users/", UserViewSet.as_view({"get": "list"}), name="user-list"),
    path("users/create/", UserViewSet.as_view({"post": "create"}), name="user-create"),
    path("users/<int:user_id>/", UserViewSet.as_view({"get": "retrieve"}), name="user-detail"),
    path("users/update/<int:user_id>/", UserViewSet.as_view({"put": "update"}), name="user-update"),
    path("users/partial-update/<int:user_id>/", UserViewSet.as_view({"patch": "partial_update"}), name="user-partial-update"),
    path("users/delete/<int:user_id>/", UserViewSet.as_view({"delete": "destroy"}), name="user-delete"),
]
