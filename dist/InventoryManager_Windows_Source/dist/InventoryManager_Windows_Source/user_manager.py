import hashlib
import os
from database import Database

class UserManager:
    def __init__(self):
        self.db = Database()

    def _hash_password(self, password):
        """Hash a password using PBKDF2 HMAC SHA256"""
        salt = os.urandom(32)  # Generate a random salt
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt.hex() + ':' + key.hex()

    def _verify_password(self, stored_password, provided_password):
        """Verify a password against its hash"""
        try:
            salt_hex, key_hex = stored_password.split(':')
            salt = bytes.fromhex(salt_hex)
            stored_key = bytes.fromhex(key_hex)
            key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
            return key == stored_key
        except ValueError:
            return False

    def authenticate(self, username, password):
        """Authenticate user login"""
        users = self.db.get_users()
        for user in users:
            if user['username'] == username and self._verify_password(user['password'], password):
                return True
        return False

    def register_user(self, username, password):
        """Register a new user"""
        hashed_password = self._hash_password(password)
        if self.db.add_user(username, hashed_password):
            return True, "User registered successfully"
        else:
            return False, "Username already exists"

    def reset_password(self, username, new_password):
        """Reset user password"""
        hashed_password = self._hash_password(new_password)
        if self.db.update_user_password(username, hashed_password):
            return True, "Password reset successfully"
        else:
            return False, "User not found"