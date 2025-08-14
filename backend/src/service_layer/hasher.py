import hashlib
import secrets


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool | None:
        if secrets.compare_digest(hashed_password, plain_password):
            return True
        return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        return hashlib.sha256(bytes(password, "utf-8")).hexdigest()
