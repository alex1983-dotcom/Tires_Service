# Проект ProffShina

## Описание приложения user_registration

Приложение `user_registration` предназначено для управления пользователями и связанными с ними сервисами в контексте 
хранения и обслуживания шин. Оно реализовано на Django и использует Django REST Framework для создания API. 
Основные функции включают:

- **Регистрация пользователей**: Позволяет новым пользователям создавать учетные записи, вводя свои данные, 
    такие как имя, фамилия, адрес электронной почты и номер телефона.
- **Аутентификация пользователей**: Обеспечивает вход в систему для зарегистрированных пользователей с помощью 
    проверки учетных данных.
- **Управление записями на обслуживание**: Пользователи могут записываться на обслуживание своих автомобилей, 
    выбирая дату и время.
- **Система скидок**: Пользователи могут получать скидки на обслуживание в зависимости от общей суммы, 
    потраченной на услуги.

### Структура приложения user_registration

1. **models.py**
 - **User**: Модель для хранения информации о пользователе, включая поля для имени, фамилии, электронной почты, 
     номера телефона и статуса активности.
 - **Discount**: Модель для хранения информации о скидках, связанных с пользователями, включая общую сумму, 
     потраченную пользователем, и процент скидки.
 - **TireStorage**: Модель для хранения информации о шинах, включая дату поступления, дату выдачи и стоимость хранения.
 - **ServiceAppointment**: Модель для записи клиентов на обслуживание, включая информацию о модели автомобиля, 
     дате и времени обслуживания.
 - **PasswordResetCode**: Модель для хранения кода сброса пароля, включая номер телефона пользователя и срок 
     действия кода.

2. **views.py**
 - **AdminLoginView**: Представление для входа администратора в систему.
 - **RegisterView**: Представление для регистрации нового пользователя.
 - **LoginView**: Представление для входа пользователя в систему.
 - **PasswordResetRequestView**: Представление для запроса сброса пароля.
 - **PasswordResetConfirmView**: Представление для подтверждения кода сброса пароля и ввода нового пароля.
 - **PersonalCabinetView**: Представление для отображения личного кабинета пользователя с информацией о скидках 
     и записях на обслуживание.
 - **API представления**: Включает представления для получения списка пользователей и записей на обслуживание.

3. **forms.py**
 - **PasswordResetRequestForm**: Форма для запроса сброса пароля по номеру телефона.
 - **PasswordResetConfirmForm**: Форма для подтверждения сброса пароля с кодом и новым паролем.
 - **UserRegistrationForm**: Форма для регистрации пользователя, включающая дополнительные поля.
 - **AdminEmailAuthenticationForm**: Форма для аутентификации администратора по электронной почте.

4. **admin.py**
 - **UserAdmin**: Настройки для управления моделью пользователя в административной панели.
 - **DiscountAdmin**: Настройки для управления моделью скидок.
 - **TireStorageAdmin**: Настройки для управления моделью хранения шин.
 - **ServiceAppointmentAdmin**: Настройки для управления моделью записей на обслуживание.

## Описание приложения forum

Приложение `forum` предназначено для создания платформы обсуждений, где пользователи могут создавать темы и сообщения. 
Оно реализовано на Django и включает в себя следующие основные функции:

### Основные функции:
- **Категории**: Пользователи могут создавать и просматривать категории, в которых будут размещены темы.
- **Темы**: Пользователи могут создавать темы обсуждений в выбранных категориях, а также просматривать существующие 
    темы.
- **Сообщения**: В каждой теме пользователи могут оставлять сообщения, отвечать на другие сообщения и просматривать 
    историю обсуждений.
- **Авторизация**: Доступ к созданию тем и сообщений ограничен для зарегистрированных пользователей.

### Структура приложения forum

1. **models.py**
 - **Category**: Модель для хранения информации о категориях форума.
 - **Thread**: Модель для представления тем обсуждений.
 - **Post**: Модель для хранения сообщений в темах.

2. **views.py**
 - **HomePageView**: Представление для отображения домашней страницы форума.
 - **CategoryListView**: Представление для отображения списка категорий.
 - **ThreadListView**: Представление для отображения списка тем в категории.
 - **PostListView**: Представление для отображения списка сообщений в теме.

3. **admin.py**
 - **ThreadAdmin**: Настройки для управления темами в административной панели.
 - **PostAdmin**: Настройки для управления сообщениями в административной панели.

## Описание приложения content

Приложение `content` отвечает за управление статьями и контентом на сайте. Оно позволяет пользователям создавать, 
редактировать и просматривать статьи, а также организовывать их по категориям. Приложение также реализовано на 
Django и использует Django REST Framework для создания API.

### Основные функции:
- **Создание статей**: Пользователи могут добавлять новые статьи с заголовками, содержимым и загружаемыми файлами.
- **Редактирование статей**: Пользователи могут изменять существующие статьи.
- **Просмотр статей**: Пользователи могут просматривать статьи по категориям и детальную информацию о каждой статье.
- **Markdown поддержка**: Содержимое статей может быть написано в формате Markdown, что позволяет легко форматировать 
    текст.

### Структура приложения content

1. **models.py**
 - **DynamicArticle**: Модель для хранения статей, включает поля для заголовка, содержания, автора, даты создания, 
     категории и файла.
 - **HomePage**: Модель для главной страницы, включает поля для заголовка, содержания, адреса, телефона и уникального 
     номера предприятия.

2. **views.py**
 - **ArticleListView**: Представление для отображения списка статей.
 - **ArticleDetailView**: Представление для отображения детальной информации об отдельной статье.
 - **ArticleCreateView**: Представление для создания новой статьи.
 - **ArticleUpdateView**: Представление для редактирования существующей статьи.

3. **admin.py**
 - **DynamicArticleAdmin**: Настройки для управления статьями в административной панели.
 - **HomePageAdmin**: Настройки для управления главной страницей в административной панели.


## Установка и запуск

1. Клонировать репозиторий:
 ```bash
 git clone <url>
 ```

2. Установить зависимости:
 ```bash
 pip install -r requirements.txt
 ```

3. Настроить переменные окружения в файле `.env`.

4. Выполнить миграции базы данных:
 ```bash
 python manage.py migrate
 ```

5. Запустить сервер разработки:
 ```bash
 python manage.py runserver
 ```

Теперь можно получить доступ к приложению по адресу 
`http://127.0.0.1:8000/`.
