from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='search'),
  path('results', views.results, name='results'),
  path('selection/<int:food_id>', views.foodItem, name='selection'),
]