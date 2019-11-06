from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),
    path('edit', views.edit),
    path('success', views.success)
]
