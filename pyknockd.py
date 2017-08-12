#!/usr/bin/env python

import socket
import sys
import os
import hashlib
import hmac
import string
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind-address", help="bind address", default="")
    parser.add_argument("-p", "--port", help="bind port", type=int, default=60120, metavar="PORT")
    parser.add_argument("psk", help="pre-shared key used to authenticate clients", metavar="PSK")
    parser.add_argument("open_cmd", help="template of command used to enable access. Example: \"ipset add -exist myset $ip\". Available variables: $ip, $port", metavar="OPEN_CMD")
    parser.add_argument("close_cmd", help="template of command used to disable access. Example: \"ipset del -exist myset $ip\". Available variables: $ip, $port", metavar="CLOSE_CMD")
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((args.bind_address, args.port))
    open_cmd = string.Template(args.open_cmd)
    close_cmd = string.Template(args.close_cmd)
    try:
        while True:
            data, addr = s.recvfrom(4096)
            ip4 = socket.inet_pton(socket.AF_INET, addr[0])
            if not data:
                continue

            opcode = data[0]
            signature = data[1:]
            if hmac.compare_digest(
                    hmac.new(
                            args.psk, opcode + ip4, hashlib.sha256
                        ).digest(),
                    signature):
                if opcode == '\x01':
                    os.system(
                        open_cmd.safe_substitute(ip = addr[0], port = addr[1])
                    )
                elif opcode == '\x02':
                    os.system(
                        close_cmd.safe_substitute(ip = addr[0], port = addr[1])
                    )
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
