import paho.mqtt.client as paho


class MqttDevice:
    def __init__(self, config):
        self.location = config['parking_lot']['location']
        self.broker = config['parking_lot']['broker_host']
        self.port = config['parking_lot']['broker_port']

        # initialise a paho client and bind it to the object
        self.client = paho.Client()
        self.client.connect(self.broker,
                            self.port)
