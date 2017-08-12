#!/usr/bin/env python

import socket
import sys
import os
import hashlib
import hmac
import string

def usage():
    print >> sys.stderr, (
            "Usage: %(progname)s <listen port> <PSK> <open command template> <close command template>\n"
            "Example:\n"
            "%(progname)s 60120 MySecretPSK 'ipset add myallowedset $ip timeout 3600' 'ipset del myallowedset $ip'"
            ) % dict(progname = sys.argv[0])
    sys.exit(2)

def main():
    if len(sys.argv) != 5:
        usage()

    port, psk, open_command_tpl, close_command_tpl = sys.argv[1:5]
    port = int(port)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", port))
    open_cmd = string.Template(open_command_tpl)
    close_cmd = string.Template(close_command_tpl)
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
                            psk, opcode + ip4, hashlib.sha256
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
