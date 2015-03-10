import phonenumbers
from pprint import pprint as pp

import csv
from re import sub
from decimal import Decimal
from netaddr import IPNetwork, IPAddress

class ServerConfigs(object):
    """server config is singleton"""
    _instance = None
    def __init__(self, file_path='server.cfg'):
        self.configs = {}
        try:
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    if not line.startswith('#'):
                        line = line.strip().split()
                        server_category = line[0].strip(',')
                        server_ips = line[1].strip(',')
                        msg_throughput = int(line[2].strip(','))
                        msg_cost = float(line[3].strip())
                        self.configs[msg_throughput] = {'category': server_category,
                                                   'ips':server_ips,
                                                   'msg_cost': msg_cost}
            invalid_cfg = False
        except Exception as exp:
            invalid_cfg, error_info = True, str(exp)
        finally:
            if not self.configs:
                invalid_cfg, error_info = True, "Invalid server configuration"
            if invalid_cfg:
                print 'Configurtation File %s Error: %s' % (file_path, error_info)
                exit(1)
        print self.configs

    def get_server_from_throughput(self, msg_throughput):
        return self.configs[msg_throughput]['ips']

    def to_dict(self):
        return self.configs

    # def __getitem__(self, key):
    #     return self.configs.get(key, None)
    #
    # def __setitem__(self, key, value):
    #     self.configs[key] = value
    #
    # def __delitem__(self, key):
    #     del self.configs[key]
    #
    # def __contains__(self, key):
    #     return key in self.configs

    def __str__(self):
        return str(self.configs)

    def __repr__(self):
        return str(self.configs)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ServerConfigs, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance


