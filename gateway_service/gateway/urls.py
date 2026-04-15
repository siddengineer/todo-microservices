from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.get_todos),
    path('add/', views.add_todo),
]