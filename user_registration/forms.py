from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'username', 'password1', 'password2']
