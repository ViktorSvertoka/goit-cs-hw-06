FROM python:3.11

WORKDIR /web_application

COPY . .

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 3000
EXPOSE 5000
EXPOSE 27017

CMD ["python3", "main.py"]


