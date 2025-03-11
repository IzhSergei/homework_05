# Указываем базовый образ Python версии 3.9
FROM python:3.12-slim-bookworm

# Устанавливаем переменные окружения для оптимизации поведения Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

#Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной исходный код приложения
# Этот слой будет пересобран каждый раз, когда изменится код приложения
COPY . .

#Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Запускаем команду для старта сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]