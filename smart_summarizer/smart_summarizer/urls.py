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
       
    # OpenAPI / Swagger/ reDocs  
    path('api/schema/',SpectacularAPIView.as_view(),name='schema',),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui',),
    path('api/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc',),


    # User Auth 
    path('api/users/register/', RegisterView.as_view(), name='user-register'),
    path('api/users/login/', LoginView.as_view(), name='user-login'),
    path('api/users/logout/', LogoutView.as_view(), name='user-logout'),

    # User CRUD 
    path('api/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('api/users/<user_id>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),

    # Document endpoints 
    path('api/documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('api/documents/', DocumentListView.as_view(), name='document-list'),
    path('api/documents/<document_id>/', DocumentDetailView.as_view(), name='document-detail'),
    path('api/documents/<document_id>/delete/', DocumentDeleteView.as_view(), name='document-delete'),
    path('api/documents/<document_id>/reparse/', DocumentReparseView.as_view(), name='document-reparse'),
]
