# myapp/urls.py
from django.urls import path
from .views import display_choices

urlpatterns = [
    path('choices/', display_choices, name='display_choices'),
]