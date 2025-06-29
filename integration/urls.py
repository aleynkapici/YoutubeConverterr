from django.urls import path
from . import views

urlpatterns = [
    path('integration/', views.integration_list_create, name='integration-list-create'),
    path('integration/<int:pk>/', views.integration_detail, name='integration-detail'),
]
