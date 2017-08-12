#!/usr/bin/env python

import sys
import socket
import hashlib
import hmac

def usage():
    print >> sys.stderr, "Usage: %s <open|close> <address> <port> <psk>" % sys.argv[0]
    sys.exit(2)

def main():
    if len(sys.argv) != 5:
        usage()

    cmd, address, port, psk = sys.argv[1:5]
    if cmd not in ('open', 'close'):
        usage()
    port = int(port)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((address, port))

    myip = socket.inet_pton(socket.AF_INET, s.getsockname()[0])
    opcode = '\x01' if cmd == 'open' else '\x02'
    digest = hmac.new(psk, opcode + myip, hashlib.sha256).digest()
    s.sendall(opcode + digest)

if __name__ == '__main__':
    main()
