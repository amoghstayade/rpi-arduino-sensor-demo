FROM python:3.8.0
WORKDIR /app
COPY requirements.txt .
COPY send_to_db.py .
COPY .env .

RUN apt-get update -y
RUN apt-get update
RUN apt-get install -y cmake
RUN pip install -r requirements.txt

CMD ["python", "send_to_dbb.py"]
