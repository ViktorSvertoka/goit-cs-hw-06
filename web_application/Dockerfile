# Використовуємо базовий образ для Python
FROM python:3.13-slim

# Встановлюємо робочу директорію
WORKDIR /web_application

# Копіюємо файли проекту в контейнер
COPY . /web_application

# Встановлюємо залежності
RUN pip install --no-cache-dir -r /web_application/requirements.txt

# Встановлюємо змінні середовища для роботи з MongoDB
ENV MONGO_PASSWORD=your_mongo_password

# Відкриваємо порти для HTTP-сервера (3000) та WebSocket-сервера (6000)
EXPOSE 3000
EXPOSE 6000

# Команда для запуску додатка
CMD ["python", "main.py"]




