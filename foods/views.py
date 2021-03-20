from django.shortcuts import render
from django.conf import settings
import requests

def search(request):
  return render(request, 'foods/search.html')

def search_results(request):
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
  return render(request, 'foods/search_results.html', context)


def foodItem(request, food_id):
  # Get nutritional data from API
  key = "api_key=" + settings.FDC_API_KEY
  url = "https://api.nal.usda.gov/fdc/v1/food/" + str(food_id) + '?' + key
  raw_data = requests.get(url)
  data = raw_data.json()

  #Extract Nutritional Data from the nutrient passed in
  def findNutrientData(inputName): 
    nutrientData = {}
    for nutrient in data['foodNutrients']:
      name = nutrient['nutrient']['name']
      if (name == inputName):    
        nutrientData['name'] = name.split(',')[0]
        nutrientData['amount'] = nutrient['amount']
        nutrientData['unit'] = nutrient['nutrient']['unitName']
        break
      else: 
        nutrientData['name'] = 'error'
        nutrientData['amount'] = 'error'
        nutrientData['unit'] = 'error'
    return nutrientData

  #Nutrients by Group
  Macros = ['Energy', 'Total lipid (fat)', 'Protein', 'Carbohydrate, by difference']
  Fats = ['Fatty acids, total saturated', 'Fatty acids, total trans', 'Cholesterol', 'Fatty acids, total monounsaturated', 'Fatty acids, total polyunsaturated']
  Carbohydrates = ['Fiber, total dietary', 'Sugars, total including NLEA']
  AminoAcids = []
  Vitamins = ['Vitamin C, total ascorbic acid', 'Thiamin', 'Riboflavin', 'Niacin', 'Pantothenic acid', 'Vitamin B-6', 'Folate, total', 'Choline, total', 'Betaine', 'Vitamin B-12', 'Vitamin A, RAE', 'Carotene, beta', 'Carotene, alpha', 'Cryptoxanthin, beta', 'Vitamin A, IU', 'Vitamin E (alpha-tocopherol)', 'Vitamin D (D2 + D3), International Units', 'Vitamin K (phylloquinone)',  ]
  Minerals = ['Calcium, Ca', 'Iron, Fe', 'Magnesium, Mg', 'Phosphorus, P', 'Potassium, K', 'Sodium, Na', 'Zinc, Zn', 'Copper, Cu', 'Manganese, Mn', 'Selenium, Se']

  #Iterate over Nutrient Groups and extract corresponding data
  def collectNutrients(Arr): 
    FoodInfo = []
    for el in Arr:
      FoodInfo.append(findNutrientData(el))
    return FoodInfo




  #Create local variable for viewing
  context = { 
    'Description': data['description'],
    'Macros': collectNutrients(Macros),
    'Vitamins': collectNutrients(Vitamins),
    'Minerals': collectNutrients(Minerals),
    'Carbohydrates': collectNutrients(Carbohydrates),
    'Fats': collectNutrients(Fats),
    'AminoAcids': collectNutrients(AminoAcids)
    }
  return render(request, 'foods/selection.html', context)