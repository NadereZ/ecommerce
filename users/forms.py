from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import CustomUser

# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2'
        ]

# User Update Form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
