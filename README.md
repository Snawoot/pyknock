pyknock
=======

UDP port knocking suite with HMAC-PSK authentication.

## Installation

Place file anywhere you want and run.

## Usage

Server example:

```bash
./pyknockd.py 60120 MySecretPSK 'ipset add -exist myallowedset $ip timeout 3600' 'ipset del -exist myallowedset $ip'
```

Client example:

```bash
./pyknock.py open my-protected-host.com 60120 MySecretPSK
```
