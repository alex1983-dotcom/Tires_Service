# Используем официальный образ Python 3.12-slim как базовый образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt /app/

# Обновляем менеджер пакетов pip до последней версии
RUN pip install --upgrade pip

# Устанавливаем зависимости, указанные в requirements.txt
RUN pip install -r requirements.txt

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . /app

# Устанавливаем команду для запуска контейнера:
# - Выполняем миграции базы данных
# - Запускаем сервер Django на всех интерфейсах (0.0.0.0) и порту 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
