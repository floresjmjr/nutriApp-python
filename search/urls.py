from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='search'),
  path('results', views.results, name='results')
]