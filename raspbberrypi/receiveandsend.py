#!/usr/bin/env python3

import serial
from azure.eventhub import EventHubProducerClient, EventData
import os
from dotenv import load_dotenv

load_dotenv()


connection_str = os.getenv('CONNECTION_STRING')
eventhub_name = os.getenv('EVENTHUB_NAME')
client = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            print("SENDING TO EVENTHUB")
            event_data_batch = client.create_batch()
            can_add = True
            while can_add:
                try:
                    event_data_batch.add(EventData(line))
                except ValueError:
                    can_add = False  # EventDataBatch object reaches max_size.

            with client:
                client.send_batch(event_data_batch)
                print("sent to eventhub")