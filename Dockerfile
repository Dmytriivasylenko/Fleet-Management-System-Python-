# Використовуємо офіційний образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо requirements.txt та встановлюємо залежності
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проект в контейнер
COPY . .

# Вказуємо команду для запуску сервера
CMD ["gunicorn", "fleet.wsgi:application", "--bind", "0.0.0.0:8000"]
