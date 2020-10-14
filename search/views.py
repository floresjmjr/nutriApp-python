from django.shortcuts import render
from django.conf import settings
import requests
import json

# Create your views here.
def home(request):
  return render(request, 'search/home.html')


def results(request):
  key = "api_key=" + settings.FDC_API_KEY
  query = "&query=" + request.GET["query"]
  database = "&dataType" + request.GET["db"]
  url = "https://api.nal.usda.gov/fdc/v1/foods/search?" + key + query + database
  raw_data = requests.get(url)
  data = json.loads(raw_data.content)
  context = {'data': data}
  return render(request, 'search/results.html', context)
