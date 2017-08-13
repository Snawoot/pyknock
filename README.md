pyknock
=======

UDP port knocking suite with HMAC-PSK authentication.

## Installation

Place file anywhere you want and run.

## Usage

Server example:

```bash
./pyknockd.py MySecretPSK 'ipset add -exist myallowedset $ip timeout 3600' 'ipset del -exist myallowedset $ip'
```

Client example:

```bash
./pyknock.py open my-protected-host.com MySecretPSK
```

Client behind NAT example:

```bash
./pyknock.py -S $(curl -s http://canihazip.com/s) open my-protected-host.com MySecretPSK
```

See help for more options.
