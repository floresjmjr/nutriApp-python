from django.urls import path
from . import views

urlpatterns = [
  path('', views.search, name='search'),
  path('search_results', views.search_results, name='search_results'),
  path('selected/<int:food_id>', views.foodItem, name='food_selected'),
]