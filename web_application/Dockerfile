FROM python:3.13-slim

WORKDIR /web_application

COPY . /web_application

RUN pip install --no-cache-dir -r /web_application/requirements.txt

EXPOSE 3000
EXPOSE 6000

CMD ["python", "main.py"]