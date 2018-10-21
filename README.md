pyknock
=======

UDP port knocking suite with HMAC-PSK authentication.

## Requirements

Only Python 2.6+ or 3.3+ required.

## Installation

Place file anywhere you want and run.

## Usage

Server example:

```bash
./pyknock-server MySecretPSK 'ipset add -exist myallowedset $ip timeout 3600' 'ipset del -exist myallowedset $ip'
```

Client example:

```bash
./pyknock-client open my-protected-host.com MySecretPSK
```

Client behind NAT example:

```bash
./pyknock-client -S $(curl -s https://canihazip.com/s) open my-protected-host.com MySecretPSK
```

See help for more options.
