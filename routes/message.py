import json
from bottle import route, run, request
from schema.v_1_0.message import MessageFactory
from schema.v_1_0.exception import RequestParameterError
import os, sys
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from msg_server_cfg import ServerConfigs

SERVER_CFG_FILE = 'server.cfg'
SERVER_CFG_PATH = os.path.join(parentddir, SERVER_CFG_FILE)

def get_server_data_from_response_routes(response_data, server_ip):
    for server_data in response_data['routes']:
        if server_ip in server_data:
            return server_data
    server_data = {server_ip:[]}
    response_data['routes'].append(server_data)
    return server_data

def create_message_response(msg, cfg_file=SERVER_CFG_PATH):
    server_cfgs = ServerConfigs(cfg_file)
    server_throughputs = sorted(server_cfgs.configs.keys(), reverse=True)
    message = msg.message
    response_data = {"message": msg.message,
                     "routes": []}
    for msg_throughput in server_throughputs:
        recipients_size = len(msg.recipients)
        while recipients_size - msg_throughput >= 0:
            server_ip = server_cfgs.get_server_from_throughput(msg_throughput)
            server_data = get_server_data_from_response_routes(response_data,
                                                               server_ip)
            for i in xrange(msg_throughput):
                server_data[server_ip].append(msg.recipients.pop())
            recipients_size = len(msg.recipients)
    return response_data


@route('/api/1.0/message', method='POST')
def create_message():
    try:
        is_error = True
        postdata = request.body.read()
        message = MessageFactory.create_message(postdata)
        is_error = False
    except RequestParameterError as err:
        message = {'error_code': '400',
                   'error_text': str(err)}
    except ValueError as err:
        message = {'error_code': '400',
                   'error_text': 'Invalid values'}
    return str(message) if is_error else create_message_response(message)

