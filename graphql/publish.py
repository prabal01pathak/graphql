import os
import sys

from azure.messaging.webpubsubservice import WebPubSubServiceClient
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':

    # if len(sys.argv) != 4:
    #     print('Usage: python publish.py <connection-string> <hub-name> <message>')
    #     exit(1)

    # connection_string = sys.argv[1]
    # hub_name = sys.argv[2]
    hub_name = "Hub"
    connection_string = os.getenv("connection_string")
    message = "Hello How are you"

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub_name)
    res = service.send_to_all(message, content_type='text/plain')
    print(res)