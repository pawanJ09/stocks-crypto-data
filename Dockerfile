FROM python:3.7.12-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN adduser app-user
RUN chown app-user /app
USER app-user

CMD ["python3", "main.py"]
