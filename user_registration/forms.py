from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class PasswordResetRequestForm(forms.Form):
    phone_number = forms.CharField(label="Номер телефона")

class PasswordResetConfirmForm(forms.Form):
    code = forms.CharField(label="Код подтверждения")
    password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтвердите новый пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя на основе UserCreationForm.
    Добавляет дополнительные поля и виджеты для улучшенного оформления.
    """

    class Meta:
        model = User
        # Поля, которые будут использоваться в форме
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'username', 'phone_number', 'password1', 'password2']
        # Настройка виджетов для полей формы
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя', 'autofocus': 'autofocus'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
        }



# class EmailAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(label='Email', max_length=254)


class AdminEmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

