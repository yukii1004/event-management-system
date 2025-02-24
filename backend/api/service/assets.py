import secrets


def unique_id():
    return secrets.randbits(32)
