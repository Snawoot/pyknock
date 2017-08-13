#!/usr/bin/env python

import sys
import socket
import hashlib
import hmac
import argparse
import time
import struct

CODE_OPEN = 1
CODE_CLOSE = 2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command: open or close", choices=["open", "close"])
    parser.add_argument("address", help="remote address", metavar="HOST")
    parser.add_argument("-p", "--port", help="remote port", type=int, default=60120)
    parser.add_argument("psk", help="pre-shared key used to authenticate ourselves to knocked peer", metavar="PSK")
    parser.add_argument("-S", "--sign-address", help="sign specified address instead of socket source address")
    parser.add_argument("-s", "--source-address", help="use following source address to send packet")
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if args.source_address:
        s.bind((args.source_address, 0))
    s.connect((args.address, args.port))

    if args.sign_address:
        myip = socket.inet_pton(socket.AF_INET, args.sign_address)
    else:
        myip = socket.inet_pton(socket.AF_INET, s.getsockname()[0])

    opcode = CODE_OPEN if args.command == 'open' else CODE_CLOSE
    msg = struct.pack('<Bd', opcode, time.time())
    digest = hmac.new(args.psk, msg + myip, hashlib.sha256).digest()
    s.sendall(msg + digest)

if __name__ == '__main__':
    main()
