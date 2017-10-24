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


def detect_af(addr):
    return socket.getaddrinfo(addr,
                              None,
                              socket.AF_UNSPEC,
                              0,
                              0,
                              socket.AI_NUMERICHOST)[0][0]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("command",
                        help="command: open or close",
                        choices=["open", "close"])
    parser.add_argument("address",
                        help="remote address",
                        metavar="HOST")
    parser.add_argument("-p",
                        "--port",
                        help="remote port",
                        type=int,
                        default=60120)
    parser.add_argument("psk",
                        help="pre-shared key "
                        "used to authenticate ourselves to knocked peer",
                        metavar="PSK")
    parser.add_argument("-S",
                        "--sign-address",
                        help="sign specified address "
                        "instead of socket source address")
    parser.add_argument("-s",
                        "--source-address",
                        help="use following source address to send packet")
    return parser.parse_args()


def panic(msg, code):
    print >> sys.stderr, msg
    sys.exit(code)
    pass


def main():
    args = parse_args()

    try:
        dst_ai = socket.getaddrinfo(args.address,
                                    args.port,
                                    socket.AF_UNSPEC,
                                    socket.SOCK_DGRAM,
                                    socket.IPPROTO_UDP)
    except Exception as e:
        print >> sys.stderr, ("Unable to resolve destination address %s: %s" %
                              (repr(args.address), str(e)))
        sys.exit(3)
    assert dst_ai, "Destionation address info must not be empty"

    src_af = socket.AF_UNSPEC
    if args.source_address:
        try:
            src_af = detect_af(args.source_address)
        except:
            panic("Malformed source address", 4)

    sign_af = socket.AF_UNSPEC
    if args.sign_address:
        try:
            sign_af = detect_af(args.sign_address)
        except:
            panic("Malformed sign address", 5)

    for ai_entry in dst_ai:
        af = ai_entry[0]
        if src_af != socket.AF_UNSPEC and af != src_af:
            continue

        s = socket.socket(af, socket.SOCK_DGRAM)
        if args.source_address:
            s.bind((args.source_address, 0))
        s.connect((ai_entry[4][0], args.port))

        if args.sign_address:
            myip = socket.inet_pton(sign_af, args.sign_address)
        else:
            myip = socket.inet_pton(af, s.getsockname()[0])

        opcode = CODE_OPEN if args.command == 'open' else CODE_CLOSE
        msg = struct.pack('<Bd', opcode, time.time())
        digest = hmac.new(args.psk, msg + myip, hashlib.sha256).digest()
        s.sendall(msg + digest)
        s.close()


if __name__ == '__main__':
    main()
