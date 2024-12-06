from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
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
import requests
import os
from .models import PasswordResetCode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
import base64  # Добавляем этот импорт

# Переменные окружения из файла .env
load_dotenv()


def send_welcome_email(user_email):
    """
    Отправляет приветственное письмо новому пользователю.

    Args:
        user_email (str): Электронная почта пользователя.
    """
    subject = 'Добро пожаловать на ProffShina!'
    message = 'Спасибо за регистрацию на нашем сайте!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


class AdminLoginView(View):
    """
    Представление для входа администратора в систему.
    """

    def get(self, request):
        """
        Отображает форму входа для администратора.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            HttpResponse: Ответ с формой входа.
        """
        form = AdminEmailAuthenticationForm()
        return render(request, 'admin/login.html', {'form': form})

    def post(self, request):
        """
        Обрабатывает POST-запрос для входа администратора.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            HttpResponse: Ответ с результатом входа.
        """
        form = AdminEmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('/admin/')
            else:
                messages.error(request, 'Недостаточно прав для доступа')
        return render(request, 'admin/login.html', {'form': form})


# Регистрация пользователя
class RegisterView(View):
    """
    Представление для регистрации пользователя.
    """

    def get(self, request):
        """
        Отображает форму регистрации.

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


# Вход в систему
class LoginView(View):
    """
    Представление для входа пользователя в систему.
    """

    def get(self, request):
        """
        Отображает форму входа.

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


# Запрос сброса пароля
class PasswordResetRequestView(View):
    """
    Представление для запроса сброса пароля.
    """

    def get(self, request):
        """
        Отображает форму запроса сброса пароля.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            HttpResponse: Ответ с формой запроса сброса пароля.
        """
        form = PasswordResetRequestForm()
        return render(request, 'user_registration/password_reset_request.html', {'form': form})

    def post(self, request):
        """
        Обрабатывает POST-запрос для запроса сброса пароля.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            HttpResponse: Ответ с результатом запроса сброса пароля.
        """
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
        Функция для отправки SMS-сообщений с использованием МТС API.

        Args:
            phone_number (str): Номер телефона получателя.
            message (str): Текст сообщения.
        """
        mts_sms_login = os.getenv('MTS_LOGIN')
        mts_sms_password = os.getenv('MTS_PASSWORD')
        mts_sms_client_id = os.getenv('MTS_CLIENT_ID')
        mts_sms_url = f'https://api.communicator.mts.by/{mts_sms_client_id}/json2/simple'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + base64.b64encode(f"{mts_sms_login}:{mts_sms_password}".encode()).decode()
        }

        # Форматируем start_time в соответствии с требованиями
        start_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S%z")
        start_time = start_time[:-2] + ':' + start_time[-2:]  # Добавляем двоеточие в часовую зону

        data = {
            'phone_number': phone_number,
            'extra_id': "AD-6640-7006",  # Пример значения, вы можете его изменить
            'callback_url': "https://api.communicator.mts.by/sms/callback",
            'start_time': start_time,
            'tag': "Password reset",
            'channels': ["sms"],
            'channel_options': {
                'sms': {
                    'text': message,
                    'ttl': 300  # Убираем alpha_name
                }
            }
        }

        try:
            response = requests.post(mts_sms_url, headers=headers, json=data, timeout=60)  # Увеличьте время ожидания до 60 секунд
            result = response.json()
            print('Response from MTS API:', result)  # Логирование полного ответа
            status = result.get('status', 'unknown')

            if status in ('SENT', 'QUEUED'):
                print('SMS accepted, status: {}'.format(status))
            else:
                print('SMS rejected, status: {}'.format(status))
        except Exception as e:
            print('Cannot send SMS: bad or no response from MTS API.')
            print(e)


class PasswordResetConfirmView(View):
    """
    Представление для подтверждения кода и ввода нового пароля.
    """

    def get(self, request):
        """
        Отображает форму для ввода нового пароля.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            HttpResponse: Ответ с формой для ввода нового пароля.
        """
        form = PasswordResetConfirmForm()
        return render(request, 'user_registration/password_reset_confirm.html', {'form': form})

    def post(self, request):
        """
        Обрабатывает POST-запрос для подтверждения кода и изменения пароля.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            HttpResponse: Ответ с результатом изменения пароля.
        """
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            reset_code = PasswordResetCode.objects.filter(code=code, expiry_date__gte=timezone.now()).first()
            if reset_code:
                try:
                    user = User.objects.get(phone_number=reset_code.phone_number)
                    user.set_password(password1)
                    user.save()
                    reset_code.delete()
                    messages.success(request, 'Ваш пароль успешно изменен.')
                    return redirect('login')
                except User.DoesNotExist:
                    messages.error(request, 'Пользователь не найден.')
            else:
                messages.error(request, 'Неверный или истекший код подтверждения.')
        return render(request, 'user_registration/password_reset_confirm.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PersonalCabinetView(View):
    """
    Представление для отображения личного кабинета пользователя.
    """

    def get(self, request):
        """
        Отображает личный кабинет пользователя.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            HttpResponse: Ответ с данными личного кабинета.
        """
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
        """
        Получает список всех записей на обслуживание.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            Response: Ответ со списком записей на обслуживание.
        """
        appointments = ServiceAppointment.objects.all()
        appointments_data = [{'user': appointment.user.username,
                              'car_model': appointment.car_model,
                              'service_date': appointment.service_date,
                              'service_time': appointment.service_time,
                              'additional_info': appointment.additional_info} for appointment in appointments]
        return Response(appointments_data)

    def post(self, request):
        """
        Создает новую запись на обслуживание.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            Response: Ответ с результатом создания записи.
        """
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
        """
        Получает информацию о конкретной записи на обслуживание.

        Args:
            request (HttpRequest): Объект запроса.
            pk (int): Идентификатор записи.

        Returns:
            Response: Ответ с данными записи или 404, если запись не найдена.
        """
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
        """
        Удаляет запись на обслуживание по идентификатору.

        Args:
            request (HttpRequest): Объект запроса.
            pk (int): Идентификатор записи.

        Returns:
            Response: Ответ с статусом удаления или 404, если запись не найдена.
        """
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
        """
        Получает список всех пользователей.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            Response: Ответ со списком пользователей.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    """
    API представление для получения информации о конкретном пользователе и его удаления.
    """

    def get(self, request, pk):
        """
        Получает информацию о конкретном пользователе.

        Args:
            request (HttpRequest): Объект запроса.
            pk (int): Идентификатор пользователя.

        Returns:
            Response: Ответ с данными пользователя или 404, если пользователь не найден.
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Удаляет пользователя по идентификатору.

        Args:
            request (HttpRequest): Объект запроса.
            pk (int): Идентификатор пользователя.

        Returns:
            Response: Ответ с статусом удаления или 404, если пользователь не найден.
        """
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
