import unittest

import smartpark.config_parser as pc


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        test_file = "test_config.toml"
        parking_lot = pc.parse_config(test_file)
        self.assertEqual(parking_lot['parking_lot']['location'], "Moondalup City Square Parking")
        self.assertEqual(parking_lot['parking_lot']['total_spaces'], 192)