import os
import sys

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib import servers
# Retire les logs
import logging
from pyftpdlib.log import config_logging

config_logging(level=logging.ERROR)


def server(user, password):
    authorizer = DummyAuthorizer()
    authorizer.add_user(user, password, './data', perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "Connection FTP by Python."

    address = ("127.0.0.1", 21)  # listen on every IP on my machine on port 21
    server = servers.FTPServer(address, handler)
    server.serve_forever(timeout=None, blocking=True, handle_exit=True, worker_processes=2)


if __name__ == '__main__':
    if sys.argv[1]:
        user=sys.argv[1]
    else:
        user="epsi"
    if sys.argv[2]:
        password = sys.argv[2]
    else:
        password = "epsi"
    server(user,password)