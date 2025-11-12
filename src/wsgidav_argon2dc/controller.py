from wsgidav import util
from wsgidav.dc.base_dc import BaseDomainController
import argon2

_logger = util.get_module_logger(__name__)
ph = argon2.PasswordHasher()

class SimpleArgon2DomainController(BaseDomainController):
  def __init__(self, wsgidav_app, config):
    super().__init__(wsgidav_app, config)

    dc_conf = util.get_dict_value(config, "argon2_dc", as_dict=True)

    self.user_map = dc_conf.get("user_mapping")
    if self.user_map is None:
      raise RuntimeError("Missing option: hash_dc.user_mapping")

    for share, data in self.user_map.items():
      if type(data) not in (bool, dict) or not data:
        raise RuntimeError(
          f"Invalid option: simple_dc.user_mapping[{share!r}]: must be True or non-empty dict."
        )
    return

  def __str__(self):
    return f"{self.__class__.__name__}()"

  def _get_realm_entry(self, realm, user_name=None):
    """Return the matching user_map entry (falling back to default '*' if any)."""
    realm_entry = self.user_map.get(realm)
    if realm_entry is None:
      realm_entry = self.user_map.get("*")
    if user_name is None or realm_entry is None:
      return realm_entry

    return realm_entry.get(user_name)

  def get_domain_realm(self, path_info, environ):
    """Resolve a relative URL to the appropriate realm name."""
    realm = self._calc_realm_from_path_provider(path_info, environ)
    return realm

  def require_authentication(self, realm, environ):
    realm_entry = self._get_realm_entry(realm)
    if realm_entry is None:
      _logger.error(
        f'Missing configuration simple_dc.user_mapping["{realm}"] (or "*"): '
        "realm is not accessible!"
      )

    return realm_entry is not True

  def basic_auth_user(self, realm, user_name, password, environ):
    """Returns True if this user_name/password pair is valid for the realm,
    False otherwise. Used for basic_authentication."""
    user = self._get_realm_entry(realm, user_name)
    if user is None or password is None:
      return False

    password_hash = user.get("password_hash").encode('utf-8')
    try:
      ph.verify(password_hash,password.encode('utf-8'))
      return True
    except argon2.exceptions.VerifyMismatchError:
      return False

  def supports_http_digest_auth(self):
    return False



