from django.contrib import admin
from django.urls import path

from user.views import LoginView, LogoutView, RegisterView, UserViewSet
from documents.views import (
    DocumentUploadView,
    DocumentListView,
    DocumentDetailView,
    DocumentDeleteView,
    DocumentReparseView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # OpenAPI / Swagger / reDocs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # User Auth
    path('users/register/', RegisterView.as_view(), name='user-register'),
    path('users/login/', LoginView.as_view(), name='user-login'),
    path('users/logout/', LogoutView.as_view(), name='user-logout'),

    # User CRUD — each action gets its own descriptive URL
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/create/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('users/<int:user_id>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('users/update/<int:user_id>/', UserViewSet.as_view({'put': 'update'}), name='user-update'),
    path('users/partial-update/<int:user_id>/', UserViewSet.as_view({'patch': 'partial_update'}), name='user-partial-update'),
    path('users/delete/<int:user_id>/', UserViewSet.as_view({'delete': 'destroy'}), name='user-delete'),

    # Document endpoints
    path('documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:document_id>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:document_id>/delete/', DocumentDeleteView.as_view(), name='document-delete'),
    path('documents/<int:document_id>/reparse/', DocumentReparseView.as_view(), name='document-reparse'),
]
