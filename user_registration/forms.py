from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    """
    Форма для регистрации пользователя
    """
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }