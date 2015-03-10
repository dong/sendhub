import unittest
import phonenumbers
import os, sys
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from msg_server_cfg import ServerConfigs
from routes.message import create_message_response
from schema.v_1_0.message import MessageFactory

server_cfgs = {1: {'category': 'Small', 'ips': '10.0.1.1', 'msg_cost': 0.01},
               5: {'category': 'Medium', 'ips': '10.0.2.1', 'msg_cost': 0.05},
              10: {'category': 'Large', 'ips': '10.0.3.1', 'msg_cost': 0.1},
              25: {'category': 'Super', 'ips': '10.0.4.1', 'msg_cost': 0.25}}
request_msg = '''{"message": "SendHubRocks", "recipients": ["8002303339",
                  "8002303338","8002303377", "8002303376", "8002303357",
                  "8002303356", "8002303355","8002303354", "8002303335",
                  "8002303352"]}'''

mock_server_cfg_file = './tests/mock.cfg'
mock_server_cfg = os.path.join(parentddir, mock_server_cfg_file)

class TestingLargeRequests(unittest.TestCase):
    def test_large_requests_succeeded(self):
        msg = MessageFactory.create_message(request_msg)
        mock_SERVER_CFGS = ServerConfigs(mock_server_cfg)
        response_msg = create_message_response(msg, mock_server_cfg)
        response_server_ip = response_msg['routes'][0].keys()[0]
        expected_server_ip = server_cfgs[10]['ips']
        self.assertTrue(response_server_ip == expected_server_ip,
                        "failed to get large ip server")

    def test_large_requests_failed(self):
        msg = MessageFactory.create_message(request_msg)
        mock_SERVER_CFGS = ServerConfigs(mock_server_cfg)
        response_msg = create_message_response(msg, mock_server_cfg)
        response_server_ip = response_msg['routes'][0].keys()[0]
        small_msgs_server_ip = server_cfgs[1]['ips']
        medium_msgs_server_ip = server_cfgs[5]['ips']
        super_msgs_server_ip = server_cfgs[25]['ips']
        wrong_servers = [small_msgs_server_ip,
                        medium_msgs_server_ip,
                        super_msgs_server_ip]
        self.assertTrue(response_server_ip not in wrong_servers,
                        "should use large msgs ip server")
