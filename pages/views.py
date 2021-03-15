from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def home(request):
  return render(request, 'pages/home.html')

def register(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    
    #Checks passwords matching
    if password == password2:
      #Checks user uniqueness
      if User.objects.filter(username=username).exists():
        #needs error message
        return redirect('register')
      else:
        # Checks email uniqueness
          if User.objects.filter(email=email).exists():
            #needs error message
            return redirect('register')
          else:
            #Creates user obj
            user = User.objects.create_user(
              username=username, 
              password=password,
              email=email,
              first_name=first_name,
              last_name=last_name
            )
            
            #Save user data and login
            user.save()
            return redirect('login')
    else:
      #needs error message
      return redirect('register')
  else:
    return render(request, 'pages/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('dashboard')
    else:
      #needs error message
      return redirect('login')

  else:
    return render(request, 'pages/login.html')

def logout(request):
  auth.logout(request)
  return redirect('home')