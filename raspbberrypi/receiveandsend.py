#!/usr/bin/env python3

import serial
from azure.eventhub import EventHubProducerClient, EventData
import os
from dotenv import load_dotenv
import sys

load_dotenv()


connection_str = os.getenv('CONNECTION_STRING')
eventhub_name = os.getenv('EVENTHUB_NAME')
client = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600)
    try:
        while True:
            try:
                line = ser.readline().decode('utf-8')
                if (line[0]!="T"):
                    print("Incomplete line")
                else:
                    print(line)
                    print("SENDING TO EVENTHUB")
                    # event_data_batch = client.create_batch()
                    # event_data_batch.add(EventData(line))
                    # with client:
                    #     client.send_batch(event_data_batch)
                    #     print("sent to eventhub")
            except:
                print("invalid line")
    except KeyboardInterrupt:
        sys.exit()
