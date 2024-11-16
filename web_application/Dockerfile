# Базовий образ
FROM python:3.11

# Встановлюємо робочу директорію
WORKDIR /web_application

# Копіюємо всі файли до контейнера
COPY . .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порти
EXPOSE 3000 5000

# Запускаємо додаток
CMD ["python", "main.py"]

