### Шаг 1: Создание приложения для регистрации пользователя
Сначала создадим новое приложение для регистрации пользователя. 
Выполните следующую команду:
```
python manage.py startapp user_registration
```


### Шаг 2: Обновите settings.py
Добавьте новое приложение в INSTALLED_APPS в `settings.py`:
```
INSTALLED_APPS = [
    ...,
    'user_registration',
]
```


### Шаг 3: Создание моделей
В `user_registration/models.py` определите модель для регистрации 
пользователя:
```
from django.db import models

class User(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email})"
```


### Шаг 4: Создание форм
Создайте форму для регистрации пользователя в `user_registration/forms.py`:
```
from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
```



### Шаг 5: Создание представлений (Views)
Создайте представления для регистрации в `user_registration/views.py`:
```
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_page')  # Редирект на главную страницу после регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration/register.html', {'form': form})
```


### Шаг 6: Создание шаблонов
Создайте шаблон для регистрации пользователя в 
`user_registration/templates/user_registration/register.html`:

```
<!DOCTYPE html>
<html>
<head>
    <title>Регистрация</title>
</head>
<body>
    <h2>Регистрация пользователя</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Зарегистрироваться</button>
    </form>
</body>
</html>
```


### Шаг 7: Добавление URL-шаблонов
Добавьте URL-шаблоны для приложения регистрации в 
`user_registration/urls.py`:

```
from django.urls import path
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
]
```

Включите URL-шаблоны нового приложения в основной конфигурации URL проекта:

```
urlpatterns = [
    ...,
    path('user/', include('user_registration.urls')),
]
```

### Шаг 8: Рассылка контента на почту
Для отправки контента на почту вам нужно настроить функцию для отправки 
писем, используя метод `send_mail` в Django.


### Шаг 9: Админка для управления скидками
Для управления скидками добавляем новую модель для обработки 
скидок в `user_registration/models.py`:

```
class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)
    
    def calculate_discount(self):
        return self.total_spent * (self.discount_rate / 100)
```

Рарегистрируйте модель в `admin.py`:

```
from django.contrib import admin
from .models import Discount

admin.site.register(Discount)
```
# Docker

### Шаг 1: Подготовка
Убедитесь, что в корневой директории вашего проекта есть файл 
`requirements.txt`. Если его нет, создайте его с помощью команды:

```bash
pip freeze > requirements.txt
```

Пример содержания:

```plaintext
Django~=5.1.2
Markdown~=3.7
```

### Шаг 2: Создание Dockerfile
Создайте файл `Dockerfile` в корневой директории проекта и добавьте в него 
следующие инструкции:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

### Шаг 3: Сборка Docker-образа
Откройте терминал в корневой директории проекта и выполните команду для 
сборки образа:

```bash
docker build -t myproject .
```

### Шаг 4: Запуск Docker-контейнера
Запустите контейнер с монтированием папок проекта:

```bash
docker run -d -p 8000:8000 -v D:\DjangoPro\ProffShina\ProffShina:/app tiresservice
```

### Шаг 5: Проверка работоспособности
Откройте браузер и перейдите по адресу:

```plaintext
http://localhost:8000
```

Если всё настроено правильно, вы должны увидеть главную страницу своего 
сайта. Чтобы просмотреть коды проекта в контейнере, подключитесь к нему:

```bash
docker exec -it <CONTAINER_ID> /bin/bash
cd /app
ls -la
```

Если у вас возникнут вопросы или потребуется 
дополнительная помощь, дайте знать! Удачи с вашим проектом! 🚀