# Базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /web_application

# Копируем все файлы в контейнер
COPY . .

# Устанавливаем виртуальное окружение и зависимости
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Открываем порты
EXPOSE 3000 6000

# Запускаем приложение
CMD ["venv/bin/python", "main.py"]


