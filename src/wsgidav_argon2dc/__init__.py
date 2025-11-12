"""A simple domain controller that stores passwords as bcrypt hashes."""

__version__ = "0.1.0"
__docformat__ = "reStructuredText"

from .controller import SimpleArgon2DomainController # noqa: F401 # type: ignore[reportUnusedImport]