from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm



# Create your views here.

def category(request, foo):
    foo = foo.replace('-', '')
    try:
        category = Category.objects.get(name=foo)
        product = Product.objects.filter(category=category)
        return redirect(request, 'store/category.html', {'product':product, 'category':category})
         
    except:
        messages.success(request,"This Category doesn't exist.")
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product.html', {'products':product})


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products':products})

def about(request):
    return render(request, 'store/about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You logged in successfully.')
            return redirect('home')
            
        else:
            messages.success(request, 'There is a problem, Please try again.')
            return redirect('login')
    else:
        return render(request, 'store/login.html', {})

   
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("You Registerd successfully."))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'store/register.html', {'form':form})
      
