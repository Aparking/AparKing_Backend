from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from .forms import LoginForm, RegisterForm
from django.http import JsonResponse
# Create your views here.
def app(request):
    return JsonResponse({'status': 'success', 'message': 'Hello, World!'})
def auth_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Usuario o contraseña incorrectos'})
        else:
            return JsonResponse({'status': 'error', 'message': str(form.errors)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer, created = CustomUser.objects.get_or_create(email=user.email, name=form.cleaned_data['name'])
            customer.user = user
            customer.save()
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': str(form.errors)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method'})

def auth_logout(request):
    logout(request)
    return JsonResponse({'status': 'success'})