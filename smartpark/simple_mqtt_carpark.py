"""An mqtt subscriber/publisher that counts cars entering and exiting a car park"""
from datetime import datetime
from config_parser import parse_config

import mqtt_device
from paho.mqtt.client import MQTTMessage


class CarPark(mqtt_device.MqttDevice):
    """Creates a car park object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['parking_lot']['total_spaces']
        self.total_cars = 0  # config['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self.client.loop_forever()
        self._temperature = None

    @property
    def available_spaces(self):
        if self.total_cars > self.total_spaces:
            # Car park is full, no negative spaces
            available = 0
        elif self.total_cars <= 0:
            # Car park is empty, no negative cars
            available = self.total_spaces
            self.total_cars = 0
        else:
            available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        
    def _publish_event(self):
        """Report data to car park, log and display"""
        readable_time = datetime.now().strftime('%H:%M')
        printout = (
            f"TIME: {readable_time}, "
            + f"CARS: {self.total_cars}, "
            + f"SPACES: {self.available_spaces}, "
            + f"TEMPC: {self.temperature}"
        )
        print(printout)

        with open("log.txt", "a") as log:
            log.write(f"{printout}\n")

        message = (
            f"TIME: {readable_time}, "
            + f"SPACES: {self.available_spaces}, "
            + f"TEMPC: {self.temperature}"
        )
        self.client.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        if self.total_cars > self.total_spaces:
            print("Car park over limit")
        self._publish_event()

    def on_car_exit(self):
        if self.total_cars == 0:
            self.total_cars = 0
            print("Exit detected while car park empty.")
            print("Check sensor for malfunction")
        else:
            self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        self.temperature = (payload.split(', ')[1])
        if 'exit' in payload:
            self.on_car_exit()
        else:
            self.on_car_entry()


if __name__ == '__main__':
    config_file = 'config.toml'
    config = parse_config(config_file)
    print("Car park initialized")
    car_park = CarPark(config)
