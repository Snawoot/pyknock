import sys
import socket
import struct
import hashlib
import hmac
import argparse


DIGEST = hashlib.sha256
DIGEST_SIZE = DIGEST().digest_size

HDR_FMT = "<%dsBdi" % (DIGEST_SIZE,)
HDR_SIZE = struct.calcsize(HDR_FMT)

CODE_OPEN = 1
CODE_CLOSE = 2


def compare_digest_polyfill(a, b):
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0


if sys.hexversion >= 0x020707F0:
    compare_digest = hmac.compare_digest
else:
    compare_digest = compare_digest_polyfill


def detect_af(addr):
    return socket.getaddrinfo(addr,
                              None,
                              socket.AF_UNSPEC,
                              0,
                              0,
                              socket.AI_NUMERICHOST)[0][0]


def check_port(value):
    ivalue = int(value)
    if not (0 < ivalue < 65536):
        raise argparse.ArgumentTypeError(
            "%s is not a valid port number" % value)
    return ivalue


def psk(value):
    if (sys.version_info > (3, 0)):
        return bytes(value, 'latin-1')
    else:
        return value
