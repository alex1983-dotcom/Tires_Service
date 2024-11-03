from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from .models import Discount, TireStorage
from django.contrib import messages

def register(request):
    """
    Представление для регистрации пользователей.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                print("Пользователь перенаправлен на личный кабинет")
                return redirect('personal_cabinet')  # Перенаправление на личный кабинет
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration/register.html', {'form': form})

def personal_cabinet(request):
    """
    Представление для личного кабинета пользователя.
    Отображает текущую скидку и информацию о хранении шин.
    """
    user = request.user
    discount = Discount.objects.get(user=user)
    tire_storages = TireStorage.objects.filter(user=user)
    return render(request, 'user_registration/personal_cabinet.html', {
        'discount': discount,
        'tire_storages': tire_storages
    })

def book_service(request):
    """
    Представление для записи автомобиля на обслуживание.
    """
    if request.method == 'POST':
        car_model = request.POST['car_model']
        service_date = request.POST['service_date']
        service_time = request.POST['service_time']
        additional_info = request.POST['additional_info']

        # Здесь можно добавить логику сохранения записи на обслуживание в базу данных

        messages.success(request, 'Вы успешно записались на обслуживание!')
        return redirect('personal_cabinet')
    return render(request, 'user_registration/book_service.html')
