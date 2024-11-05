from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from .models import Discount, TireStorage, ServiceAppointment
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user_email):
    subject = 'Добро пожаловать на ProffShina!'
    message = 'Спасибо за регистрацию на нашем сайте!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


def register(request):
    """
    Представление для регистрации пользователей.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)  # Убедимся, что пароль установлен
            user.save()
            user = authenticate(username=user.email, password=raw_password)
            if user is not None:
                login(request, user)
                print("Пользователь аутентифицирован, перенаправление на личный кабинет")
                return redirect('personal_cabinet')
            else:
                print("Ошибка аутентификации")
        else:
            print("Форма невалидна")
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('personal_cabinet')
        else:
            messages.error(request, 'Неверный email или пароль')
    return render(request, 'user_registration/login.html')


def personal_cabinet(request):
    """
    Представление для личного кабинета пользователя.
    Отображает текущую скидку и информацию о хранении шин.
    """
    user = request.user
    try:
        discount = Discount.objects.get(user=user)
    except Discount.DoesNotExist:
        discount = None

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
