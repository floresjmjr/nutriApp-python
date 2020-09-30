from django.urls import path
from . import views

urlpatterns = [
  path('', views.daily, name='daily_log'),
]