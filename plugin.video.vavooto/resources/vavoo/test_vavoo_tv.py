import unittest
from unittest.mock import patch
import json
import requests
from vavoo.vavoo_tv import vavoo_groups, new_vav_channels, get_vav_channels

class TestVavooTV(unittest.TestCase):
    @patch('vavoo.vavoo_tv.requests.get')
    def test_vavoo_groups(self, mock_get):
        mock_response = '[{"group": "Sunshine", "name": "Test1"}, {"group": "Smoke", "name": "Test2"}]'
        mock_get.return_value.text = mock_response
        groups, hashval = vavoo_groups()
        self.assertIn('Sunshine', groups)
        self.assertIn('Smoke', groups)
        self.assertIsInstance(hashval, str)

    @patch('vavoo.vavoo_tv.requests.post')
    def test_new_vav_channels(self, mock_post):
        mock_post.return_value.json.return_value = {
            "items": [
                {"url": "http://test/stream1", "name": "Sunshine Stream", "group": "Sunshine"},
                {"url": "http://test/stream2", "name": "Smoke Stream", "group": "Smoke"}
            ],
            "nextCursor": None
        }
        items = new_vav_channels("Sunshine")
        self.assertTrue(any('Sunshine' in i['group'] for i in items))

    @patch('vavoo.vavoo_tv.get_cache', return_value=(True, ["Sunshine"]))
    @patch('vavoo.vavoo_tv.vavoo_groups', return_value=(['Sunshine', 'Smoke'], 'dummyhash'))
    @patch('vavoo.vavoo_tv.set_cache')
    @patch('vavoo.vavoo_tv.new_vav_channels', return_value=[{"url": "http://test/stream1", "name": "Sunshine Stream", "group": "Sunshine"}])
    def test_get_vav_channels(self, mock_new, mock_set, mock_groups, mock_cache):
        vavchannels = get_vav_channels(["Sunshine"])
        self.assertIn("Sunshine Stream", vavchannels)
        self.assertTrue(any("http://test/stream1" in urls for urls in vavchannels.values()))

if __name__ == '__main__':
    unittest.main()
