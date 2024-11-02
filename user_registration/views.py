from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration/register.html', {'form': form})
