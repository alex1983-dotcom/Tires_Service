from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .forms import PasswordResetRequestForm, PasswordResetConfirmForm
from .forms import UserRegistrationForm
from .models import Discount, TireStorage, ServiceAppointment, User
from .serializers import UserSerializer
from .forms import AdminEmailAuthenticationForm
from django.utils.decorators import method_decorator
from dotenv import load_dotenv
from django.utils.crypto import get_random_string
from django.utils import timezone
import os
from .models import PasswordResetCode
import requests

# Переменные окружения из файла .env
load_dotenv()


def send_welcome_email(user_email):
    """
    Отправляет приветственное письмо новому пользователю.
    """
    subject = 'Добро пожаловать на ProffShina!'
    message = 'Спасибо за регистрацию на нашем сайте!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


class AdminLoginView(View):
    def get(self, request):
        form = AdminEmailAuthenticationForm()
        return render(request, 'admin/login.html', {'form': form})

    def post(self, request):
        form = AdminEmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('/admin/')
            else:
                messages.error(request, 'Недостаточно прав для доступа')
        return render(request, 'admin/login.html', {'form': form})


class RegisterView(View):
    """
    Представление для регистрации пользователя.
    """
    def get(self, request):
        """
        Обрабатывает GET-запрос для отображения формы регистрации.
        Args:
            request (HttpRequest): Объект запроса.
        Returns:
            HttpResponse: Ответ с формой регистрации.
        """
        form = UserRegistrationForm()
        return render(request, 'user_registration/register.html', {'form': form})

    def post(self, request):
        """
        Обрабатывает POST-запрос для регистрации нового пользователя.
        Args:
            request (HttpRequest): Объект запроса.
        Returns:
            HttpResponse: Ответ с результатом регистрации.
        """
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                raw_password = form.cleaned_data.get('password1')
                user.set_password(raw_password)  # Устанавливаем пароль пользователя
                user.save()
                # Аутентификация пользователя после регистрации
                user = authenticate(username=user.phone_number, password=raw_password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Регистрация прошла успешно!')
                    return redirect('personal_cabinet')
                else:
                    messages.error(request, 'Ошибка аутентификации.')
            except Exception as e:
                messages.error(request, f"Ошибка при регистрации: {str(e)}")
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        return render(request, 'user_registration/register.html', {'form': form})


class LoginView(View):
    """
    Представление для входа пользователя в систему.
    """
    def get(self, request):
        """
        Обрабатывает GET-запрос для отображения формы входа.
        Args:
            request (HttpRequest): Объект запроса.
        Returns:
            HttpResponse: Ответ с формой входа.
        """
        return render(request, 'user_registration/login.html')

    def post(self, request):
        """
        Обрабатывает POST-запрос для аутентификации пользователя.
        Args:
            request (HttpRequest): Объект запроса.
        Returns:
            HttpResponse: Ответ с результатом аутентификации.
        """
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('personal_cabinet')
        else:
            messages.error(request, 'Неверный номер телефона или пароль')
        return render(request, 'user_registration/login.html')


class PasswordResetRequestView(View):
    """
    Представление для запроса сброса пароля.
    """
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, 'user_registration/password_reset_request.html', {'form': form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            # Генерируем код и отправляем SMS
            code = get_random_string(length=6, allowed_chars='0123456789')
            expiry_date = timezone.now() + timezone.timedelta(minutes=10)
            PasswordResetCode.objects.create(phone_number=phone_number, code=code, expiry_date=expiry_date)
            self.send_sms(phone_number, f"Ваш код для сброса пароля: {code}")
            messages.success(request, 'Код для сброса пароля отправлен на ваш номер телефона.')
            return redirect('password_reset_confirm')
        return render(request, 'user_registration/password_reset_request.html', {'form': form})

    def send_sms(self, phone_number, message):
        """
        Функция для отправки SMS - сообщений с использованием API МТС.
        """
        mts_api_url = 'https://api.mts.by/sms/send' # заменить на реальный URL
        account_sid = os.getenv('MTS_ACCOUNT_SID')
        auth_token = os.getenv('MTS_AUTH_TOKEN')

        payload = {
            'account_sid': account_sid,
            'auth_token': auth_token,
            'to':phone_number,
            'body': message
        }

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(mts_api_url, json=payload, headers=headers)

        if response.status_code == 200:
            print("SMS успешно отправлено")
        else:
            print(f"Ошибка при отправке SMS: {response.status_code} - {response.text}")


class PasswordResetConfirmView(View):
    """
    Представление для подтверждения кода и ввода нового пароля.
    """
    def get(self, request):
        form = PasswordResetConfirmForm()
        return render(request, 'user_registration/password_reset_confirm.html', {'form': form})

    def post(self, request):
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            reset_code = PasswordResetCode.objects.filter(code=code, expiry_date__gte=timezone.now()).first()
            if reset_code and reset_code.is_valid():
                user = User.objects.get(phone_number=reset_code.phone_number)
                user.set_password(password1)
                user.save()
                reset_code.delete()
                messages.success(request, 'Ваш пароль успешно изменен.')
                return redirect('login')
            else:
                messages.error(request, 'Неверный или истекший код подтверждения.')
        return render(request, 'user_registration/password_reset_confirm.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PersonalCabinetView(View):
    """
    Представление для отображения личного кабинета пользователя.
    """

    def get(self, request):
        user = request.user

        # Получаем скидку пользователя, если она есть
        try:
            discount = Discount.objects.get(user=user)
        except Discount.DoesNotExist:
            discount = None

        # Получаем записи на обслуживание для текущего пользователя, сортируем по дате и берем последние две
        appointments = ServiceAppointment.objects.filter(user=user).order_by('-service_date')[:2]

        # Получаем информацию о хранении шин
        tire_storages = TireStorage.objects.filter(user=user)

        return render(request, 'user_registration/personal_cabinet.html', {
            'user': user,
            'discount': discount,
            'tire_storages': tire_storages,
            'appointments': appointments,  # Передаем последние две записи на обслуживание в контекст
        })


class ServiceAppointmentListView(APIView):
    """
    API представление для получения списка всех записей на обслуживание и создания новой записи.
    """
    def get(self, request):
        appointments = ServiceAppointment.objects.all()
        appointments_data = [{'user': appointment.user.username,
                              'car_model': appointment.car_model,
                              'service_date': appointment.service_date,
                              'service_time': appointment.service_time,
                              'additional_info': appointment.additional_info} for appointment in appointments]
        return Response(appointments_data)

    def post(self, request):
        user = request.user
        car_model = request.data.get('car_model')
        service_date = request.data.get('service_date')
        service_time = request.data.get('service_time')
        additional_info = request.data.get('additional_info', '')

        appointment = ServiceAppointment(user=user, car_model=car_model,
                                         service_date=service_date, service_time=service_time,
                                         additional_info=additional_info)
        appointment.save()
        return Response({'status': 'Запись создана'}, status=status.HTTP_201_CREATED)


class ServiceAppointmentDetailView(APIView):
    """
    API представление для получения информации о конкретной записи на обслуживание и её удаления.
    """
    def get(self, request, pk):
        try:
            appointment = ServiceAppointment.objects.get(pk=pk)
            appointment_data = {'user': appointment.user.username,
                                'car_model': appointment.car_model,
                                'service_date': appointment.service_date,
                                'service_time': appointment.service_time,
                                'additional_info': appointment.additional_info}
            return Response(appointment_data)
        except ServiceAppointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            appointment = ServiceAppointment.objects.get(pk=pk)
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ServiceAppointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserListView(APIView):
    """
    API представление для получения списка всех пользователей.
    """
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    """
    API представление для получения информации о конкретном пользователе и его удаления.
    """
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

