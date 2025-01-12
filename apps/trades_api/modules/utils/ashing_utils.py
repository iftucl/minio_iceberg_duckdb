import base64
import hashlib
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

HASH_SALT = "c1dc1a1449222f41331976fda2cd7866510d2a171849d75bca6492d55b757fbe59fe6a04e86870460ea0a2ce81c917feb3b584d197b94d964c9450e38393acc3"
HASH_KEY = "c1dc1a1449222f41331976fda2cd7866510d2a171849d75bca6492d55b757fbe59fe6a04e86870460ea0a2ce81c917feb3b584d197b94d964c9450e38393acc3"


def create_ash_key(key_size: int):
    """
    Generates a hashing key.

    :param key_size: Numeric 64, 32, ...
    :type key_size: int
    :return: Returns a hexadecimal key
    :rtype: str
    """
    _key = os.urandom(key_size)
    return _key.hex()

def create_ash_salt(salt_size: int):
    """
    Generates salt.

    :param salt_size: Size of salt
    :type salt_size: int
    :return: Returns salt in hexadecimal
    :rtype: str
    """
    _salt = os.urandom(salt_size)
    return _salt.hex()

class HashingTool:
    """
    Hashing functionality.

    Hashes data provided using key and salt.
    """

    def __init__(self, key: str, salt: str, data: str):
        """
        Constructor.

        :param key: A hexadecimal key.
        :type key: str
        :param salt: A hexadecimal salt.
        :type salt: str
        :param data: Data to be hashed.
        :type data: str
        """
        self._key = bytes.fromhex(key)
        self._salt = bytes.fromhex(salt)
        self.hashed = self.hashit(data.encode())

    def hashit(self, data):
        """Hashes data provided."""
        data_with_salt = self._salt + data
        # Hash the new data with the stored key and salt
        h = hashlib.blake2b(key=self._key)
        h.update(data_with_salt)
        digest = h.hexdigest()
        return digest

    def __eq__(self, hasher):
        return self.hashed == hasher.hashed

    def __ne__(self, hasher):
        return self.hashed != hasher.hashed



def password_hashing(plain_text: str):
    hash_object = HashingTool(key=HASH_KEY, salt=HASH_SALT, data=plain_text)
    return hash_object.hashed
