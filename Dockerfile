FROM python:3.9.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN adduser app-user
USER app-user

CMD ["python3", "main.py"]
