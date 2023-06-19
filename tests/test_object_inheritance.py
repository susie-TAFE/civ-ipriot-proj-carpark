"""Tests to ensure Sensor class is initializing and inheriting correctly"""
import unittest

import smartpark.simple_mqtt_sensor as sensor_file
import smartpark.config_parser as parser


class TestObjectAndInheritance(unittest.TestCase):
    def get_config_data(self):
        # get the configuration data from a file
        test_file = "test_config.toml"
        return parser.parse_config(test_file)

    def test_sensor_object_is_initialized(self):
        test_sensor = sensor_file.Sensor(self.get_config_data())
        self.assertTrue((type(test_sensor)), "<class 'smartpark.simple_mqtt_sensor.Sensor'>")

    def test_sensor_object_inherits_from_mqtt_device(self):
        test_sensor = sensor_file.Sensor(self.get_config_data())
        self.assertEqual(test_sensor.location, "Moondalup City Square Parking")


if __name__ == '__main__':
    unittest.main()
