#!/usr/bin/env python

import socket
import sys
import os
import hashlib
import hmac
import string
import argparse
import struct
import time

DIGEST = hashlib.sha256
DIGEST_SIZE = DIGEST().digest_size
BODY_SIZE = 1 + 8
MSG_SIZE = BODY_SIZE + DIGEST_SIZE
CODE_OPEN = 1
CODE_CLOSE = 2
MSG_FMT = "<Bd%ds" % (DIGEST_SIZE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind-address", help="bind address", default="")
    parser.add_argument("-p", "--port", help="bind port", type=int, default=60120, metavar="PORT")
    parser.add_argument("-t", "--time-drift", help="allowed time drift in seconds between client and server. Value may be a floating point number", type=float, default=60, metavar="DRIFT")
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

            if len(data) != MSG_SIZE:
                continue

            opcode, ts, digest = struct.unpack(MSG_FMT, data)

            if abs(ts - time.time()) > args.time_drift:
                continue

            if not hmac.compare_digest(
                    hmac.new(
                            args.psk, data[:BODY_SIZE] + ip4, DIGEST
                        ).digest(),
                    digest):
                continue

            if opcode == CODE_OPEN:
                os.system(
                    open_cmd.safe_substitute(ip = addr[0], port = addr[1])
                )
            elif opcode == CODE_CLOSE:
                os.system(
                    close_cmd.safe_substitute(ip = addr[0], port = addr[1])
                )
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
