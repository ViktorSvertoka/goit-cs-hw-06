FROM python:3.10

ENV directory /new_directory

WORKDIR $directory

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000
EXPOSE 6000
EXPOSE 27017

ENTRYPOINT ["python", "main.py"]


