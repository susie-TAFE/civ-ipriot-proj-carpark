import paho.mqtt.client as paho

BROKER, PORT = "localhost", 1883

client = paho.Client()
client.connect(BROKER, PORT)
client.publish("lot/sensor", "Hello from Python")

# test that Display is receiving and correctly formatting a message.
message_for_display = "Available Spaces: 196,Temperature: 23C,Current Time: 09:00"
client.publish("display", message_for_display)
