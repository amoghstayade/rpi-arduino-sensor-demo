FROM python:3.9
WORKDIR /app
COPY /home/pi/Desktop/DHT11_project/rpi-arduino-sensor-demo/raspbberrypi/requirements.txt .
COPY /home/pi/Desktop/DHT11_project/rpi-arduino-sensor-demo/raspbberrypi/send_to_eventhub.py .

RUN pip install -r requirements.txt

CMD ["python", "send_to_eventhub.py"]