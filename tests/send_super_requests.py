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
request_msg = '''{"message": "SendHubRocks", "recipients": ["8002303330",
              "8002303372", "8002303333", "8002303378", "8002303332", "8002303326",
              "8002303327", "8002303324", "8002303325", "8002303322", "8002303323",
              "8002303320", "8002303321", "8002303362", "8002303363", "8002303360",
              "8002303361", "8002303366", "8002303367", "8002303328", "8002303329",
              "8002303340", "8002303341", "8002303342", "8002303343", "8002303344",
              "8002303345", "8002303346", "8002303347", "8002303348", "8002303349",
              "8002303375", "8002303374", "8002303380", "8002303364", "8002303373",
              "8002303365", "8002303353", "8002303313", "8002303312", "8002303337",
              "8002303336", "8002303317", "8002303316", "8002303315", "8002303314",
              "8002303371", "8002303370", "8002303319", "8002303318"]}'''


mock_server_cfg_file = './tests/mock.cfg'
mock_server_cfg = os.path.join(parentddir, mock_server_cfg_file)

class TestingSuperRequests(unittest.TestCase):
    def test_super_requests_succeeded(self):
        msg = MessageFactory.create_message(request_msg)
        mock_SERVER_CFGS = ServerConfigs(mock_server_cfg)
        response_msg = create_message_response(msg, mock_server_cfg)
        response_server_ip = response_msg['routes'][0].keys()[0]
        expected_server_ip = server_cfgs[25]['ips']
        self.assertTrue(response_server_ip == expected_server_ip,
                        "failed to get super msgs ip server")

    def test_super_requests_failed(self):
        msg = MessageFactory.create_message(request_msg)
        mock_SERVER_CFGS = ServerConfigs(mock_server_cfg)
        response_msg = create_message_response(msg, mock_server_cfg)
        response_server_ip = response_msg['routes'][0].keys()[0]
        small_msgs_server_ip = server_cfgs[1]['ips']
        medium_msgs_server_ip = server_cfgs[5]['ips']
        large_msgs_server_ip = server_cfgs[10]['ips']
        wrong_servers = [small_msgs_server_ip,
                        medium_msgs_server_ip,
                        large_msgs_server_ip]
        self.assertTrue(response_server_ip not in wrong_servers,
                        "should use super msgs ip server")
