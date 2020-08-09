pyknock
=======

UDP port knocking suite with HMAC-PSK authentication. Once it receives valid packet signed with valid pre-shared key, it runs command to open or close access. Commands should be specified by user via server command line. Server allows use of substitution placeholders in configured commands:

* `$ip` - IP address mentioned in signed packet
* `$af` - IP address type: `inet` or `inet6`
* `$cmd` - requested action: `open` or `close`

See Usage for examples.

---

:heart: :heart: :heart:

You can say thanks to the author by donations to these wallets:

- ETH: `0xB71250010e8beC90C5f9ddF408251eBA9dD7320e`
- BTC:
  - Legacy: `1N89PRvG1CSsUk9sxKwBwudN6TjTPQ1N8a`
  - Segwit: `bc1qc0hcyxc000qf0ketv4r44ld7dlgmmu73rtlntw`

---

## Main Idea

In this application UDP datagrams are choosen for a reason. Typical configuration of firewalled machine allows only packets to some public ports and drops packets to all other ports. With UDP external observer can't distinguish between accepted packet and packet dropped by firewall. Therefore, if firewall configuration drops all UDP packets except packets to pyknock port, external observer can't even detect there is something awaiting for magic packet. So, it may be used to hide machine completely from network for unauthenticated peers. Also, it may be used as classical port-knocking solution, adding another protection layer to sensitive network application.

## Features

* Uses cryptographically authenticated messages.
* Resistant to replay attacks.
* Post-quantum ready cryptography (HMAC-PSK with SHA-256).
* Works completely in user-space. May run even as unprivileged user.

## Requirements

Only Python 2.6+ required. Python 3 is also supported.

## Installation

Place file anywhere you want and run. Or use `pip install pyknock` to install it into your system as python package. Scripts shall become available at standard binary paths.

## Usage

Server example:

```bash
pyknock-server MySecretPSK 'ipset add -exist myallowedset $ip timeout 3600' 'ipset del -exist myallowedset $ip'
```

Client example:

```bash
pyknock-client open my-protected-host.com MySecretPSK
```

Client behind NAT example:

```bash
pyknock-client -S $(curl -s https://canihazip.com/s) open my-protected-host.com MySecretPSK
```

See help for more options.
