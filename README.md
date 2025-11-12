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

Tested to  work with wsgidav 4.3.3