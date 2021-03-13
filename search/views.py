from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.
def home(request):
  return render(request, 'search/home.html')


def results(request):
  key = "api_key=" + settings.FDC_API_KEY
  query = "&query=" + request.GET["query"]
  database = "&dataType=" + request.GET["db"]
  resultSize = "&pageSize=" + "20"
  url = "https://api.nal.usda.gov/fdc/v1/foods/search?" + key + query + database + resultSize
  raw_data = requests.get(url)
  data = raw_data.json()
  
  hits = True if int(data['totalHits']) > 0 else False
  query = data['foodSearchCriteria']['query']
  context = {
    'hits': hits,
    'query': query,
    'foodList': data['foods'],
    }
  return render(request, 'search/results.html', context)


def foodItem(request, food_id):
  key = "api_key=" + settings.FDC_API_KEY
  url = "https://api.nal.usda.gov/fdc/v1/food/" + str(food_id) + '?' + key
  raw_data = requests.get(url)
  data = raw_data.json()
  context = { 
    'Description': data['description'],
    'Calories': data['foodNutrients'][0]['nutrient']['name']
    }
  return render(request, 'search/selection.html', context)

