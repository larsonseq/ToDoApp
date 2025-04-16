from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, LoginForm
from category.models import Category  # Assuming you have a Category model

# Define the categories that need to be checked and created
DEFAULT_CATEGORIES = ['Work', 'Personal', 'Shopping']

# Function to check and create default categories
def check_and_create_categories():
    for category_name in DEFAULT_CATEGORIES:
        if not Category.objects.filter(name=category_name).exists():
            Category.objects.create(name=category_name)

def logout_view(request):
    logout(request)
    return redirect('main')

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Check and create categories if they don't exist
                check_and_create_categories()

                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('todolist:my_todos')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)

def registerUserView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            
            if user is not None:
                login(request, user)

                # Check and create categories if they don't exist
                check_and_create_categories()

                return redirect('todolist:my_todos')
    
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'auth/register.html', context)
