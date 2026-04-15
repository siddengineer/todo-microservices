from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.get_todos),
    path('add/', views.add_todo),
    path('update/<int:id>/', views.update_todo),
    path('delete/<int:id>/', views.delete_todo),
]