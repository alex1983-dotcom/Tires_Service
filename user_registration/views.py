from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User

def register(request):
    """
    Представление для регистрации пользователя
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')  # Редирект на главную страницу после регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration/register.html', {'form': form})