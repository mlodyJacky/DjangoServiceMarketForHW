from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.search_users, name='items'),  # Przykładowa ścieżka
]

