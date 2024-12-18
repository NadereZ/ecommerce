from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm
from rest_framework import viewsets
from . models import CustomUser
from . serializers import UserSerializers
from rest_framework.permissions import IsAuthenticated

# User Registration
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('profile')  # Redirect to profile after registration
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Login successful.")
        return super().form_valid(form)

# Logout User
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# User Profile
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error updating your profile.")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

# User api
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated]