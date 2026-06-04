import bcrypt

CANNOT_BE_EMPTY = "Password cannot be empty"


def hash_password(password: str) -> str:
    """Password Hashing"""
    if not password:
        raise ValueError(CANNOT_BE_EMPTY)

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")
