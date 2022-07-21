# rpi-arduino-sensor-demo
Demo project to display RPI, arduino and Azure combinations for IoT applications

* ### **Architecture of the project:**
https://drive.google.com/file/d/10gf7Q58NxgS6JjXQNH0WHzFQdLnI9Gn-/view?usp=sharing
![alt text](ArduinoRPiProject.drawio.svg)


In raspberry pi, to get the docker container to read directly from physical device(arduino), while running docker container, pass in the device name. 
Example - sudo docker build . -t image_name
docker run -it --device=/dev/ttyACM0 image_name


# Commands
docker build -t send_to_eventhub .
docker run -it --device=/dev/ttyACM0 image_name