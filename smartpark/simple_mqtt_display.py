import mqtt_device
import time
from datetime import datetime
from config_parser import parse_config


class Display(mqtt_device.MqttDevice):
    """Displays the number of cars and the temperature"""
    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.client.loop_forever()

    def display(self, *args):
        print('*' * 20)
        for val in args:
            print(val)
            time.sleep(1)

        print('*' * 20)

    def parse_values(self, message) -> dict:
        value_strings = message.split(', ')  # split message to a list
        values = {}
        for i in value_strings:
            key = (i.split(': ')[0])
            value = i.split(': ')[1]
            values[key] = value
        return values

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()
        values = self.parse_values(data)
        time = datetime.strptime((values['TIME']), '%H:%M').time()
        temperature = int(values['TEMPC'])
        free_spaces = int(values['SPACES'])
        display_values = \
            f"SPACES: {free_spaces}", \
            f"TEMPC:  {temperature}", \
            f"TIME:   {time.strftime('%H:%M')}"
        self.display(*display_values)


if __name__ == '__main__':
    config_file = 'config.toml'
    config = parse_config(config_file)
    print("Display initialized")
    display = Display(config)
