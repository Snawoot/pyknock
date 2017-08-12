#!/usr/bin/env python

import sys
import socket
import hashlib
import hmac
import argparse

#def usage():
#    print >> sys.stderr, "Usage: %s <open|close> <address> <port> <psk>" % sys.argv[0]
#    sys.exit(2)
#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command: open or close", choices=["open", "close"])
    parser.add_argument("address", help="remote address")
    parser.add_argument("port", help="remote port", type=int)
    parser.add_argument("psk", help="pre-shared key used to authenticate ourselves to knocked peer")
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((args.address, args.port))

    myip = socket.inet_pton(socket.AF_INET, s.getsockname()[0])
    opcode = '\x01' if args.command == 'open' else '\x02'
    digest = hmac.new(args.psk, opcode + myip, hashlib.sha256).digest()
    s.sendall(opcode + digest)

if __name__ == '__main__':
    main()
