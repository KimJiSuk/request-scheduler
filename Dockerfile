FROM python:3.8-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host python.org -r requirements.txt

CMD ["python", "-u", "main.py"]
