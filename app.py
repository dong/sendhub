import json
from bottle import run
from routes.message import *

SERVER_PORT = 8080

run(host='localhost', port=SERVER_PORT, debug=True)
