# wsgidav-argon2dc

An implementation of the [wsgidav](https://wsgidav.readthedocs.io/en/latest/index.html) simple-dc that uses argon2id hashes instead of plain text passwords.


## Installation

Tested installation method:
```shell
$ pip install -e .
```

## Configuration

Configuration is basically the same as for the [simple-dc](https://wsgidav.readthedocs.io/en/latest/user_guide_configure.html#simpledomaincontroller), with the exception that it uses the `argon2_dc` instead of `simple_dc` config key, and a `password_hash` property is used instead of `password`.
I could not find where `simple_dc` set it's `/:dir_browser` to anonymous to allow it to bypass authentication. I did not want anonymous access either so I chose to add user mapping for `/:dir_browser` into the config as well.

```yaml
# NOTE: only HTTP basic auth is supported, make sure your communication to the wsgidav service is using SSL encryption
http_authenticator:
    domain_controller: wsgidav_argon2dc.SimpleArgon2DomainController
    accept_basic: true
    accept_digest: false
    default_to_digest: false

argon2_dc:
    user_mapping:
        '*': # default user mapping for all shares
            'username':
                password_hash: '$argon2id$v=19$m=65536,t=3,p=4$l6VYjn/pa3338w8bHUwRrQ$6/ys/lv2yvibB5jsQ988ZyRG2u1eIl6wgxUpFtz76So' # argon2id hash for 'newpass1'
                roles: ['admin']
        '/:dir_browser': # Separately define users allowed to use dir_browser
            'username':
                password_hash: '$argon2id$v=19$m=65536,t=3,p=4$l6VYjn/pa3338w8bHUwRrQ$6/ys/lv2yvibB5jsQ988ZyRG2u1eIl6wgxUpFtz76So' # argon2id hash for 'newpass1'
                roles: ['admin']
```

Tested to  work with wsgidav 4.3.3 using cheroot

## Utilities

`hash_gen_ver.py` is provided as an utility to generate and verify your hashes for your intended password.

```bash
usage: hash_gen_ver.py [-h] [-v] [-d] [-c CUSTOMHASHER] [-ph PWDHASH]

options:
  -h, --help            show this help message and exit
  -v, --verify          Turn on verify mode to verify hash
  -d, --debug           Turn on debug mode for printing debug messages
  -c CUSTOMHASHER, --customhasher CUSTOMHASHER
                        Pass parameters to customise Hasher parameters as per argon2-cffi CLI interface. Separate options and values with `,` eg t,1,m,524288,p,4
  -ph PWDHASH, --pwdhash PWDHASH
                        Enter hash to be verified with this flag
```

## Choosing hashing parameters

See [argon2-cffi](https://argon2-cffi.readthedocs.io/en/stable/parameters.html) recommendations for choosing parameters and [RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html#name-parameter-choice) standard for suggested default parameters.

argon2-cffi provides a [CLI](https://argon2-cffi.readthedocs.io/en/stable/cli.html) interface for benchmarking your chosen settings. `hash_gen_ver.py` allows the same parameter options as this CLI ie -t for time, -m for memory, -p for parallelism, -l for hash length. This should be enough to tweak based on the general recommended check list below with the goal of about 500ms to verify a hash:
1. Start with 4 for parallelism and the an amount of memory available for it.
2. Try different time cost options for it that still meets your goal of how long verification should take.
3. If this time is still exceeded with time value `1` then reduce the memory parameter.

RFC 9106 recommends: hash_len(l)=`32`, time_cost(t)=`1`, memory_cost(m)=`2097152` (2GiB), parallelism(p)=`4`
while argon2-cffi defaults to : hash_len(l)=`32` time_cost(t)=`3`, memory_cost(m)=`65536` (64 MiB), parallelism(p)=`4`
The argon2-cffi defaults are the secondary recommendation for devices with limited memory.