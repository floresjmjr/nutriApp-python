from django.shortcuts import render


def log(request):
  user = request.user
  context = {
    'user': user
  }
  return render(request, 'dashboard/log.html')

def charts(request):
  return render(request, 'dashboard/charts.html')