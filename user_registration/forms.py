from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class PasswordResetRequestForm(forms.Form):
    """
    Форма для запроса сброса пароля по номеру телефона.
    """
    phone_number = forms.CharField(label="Номер телефона", max_length=15)

    def clean_phone_number(self):
        """
        Проверка валидности номера телефона.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError("Номер телефона обязателен.")
        if not phone_number.isdigit() or len(phone_number) < 10:
            raise forms.ValidationError("Введите корректный номер телефона.")
        return phone_number


class PasswordResetConfirmForm(forms.Form):
    """
    Форма для подтверждения сброса пароля с кодом и новым паролем.
    """
    code = forms.CharField(label="Код подтверждения", max_length=6)
    password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтвердите новый пароль", widget=forms.PasswordInput)

    def clean(self):
        """
        Проверка совпадения нового пароля и подтверждения.
        """
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
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'username', 'phone_number', 'password1', 'password2']
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

    def clean_email(self):
        """
        Проверка уникальности email.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email

    def clean_phone_number(self):
        """
        Проверка уникальности номера телефона.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Этот номер телефона уже используется.")
        return phone_number

class AdminEmailAuthenticationForm(AuthenticationForm):
    """
    Форма аутентификации администратора по email.
    """
    username = forms.EmailField(label='Email', max_length=254)

    def confirm_login_allowed(self, user):
        """
        Проверка, разрешен ли вход пользователя.
        """
        if not user.is_active:
            raise forms.ValidationError("Этот аккаунт неактивен.")
        if not user.is_staff:
            raise forms.ValidationError("Доступ разрешен только администраторам.")
