from cryptography.fernet import Fernet
from config import config


async def get_key():
    decoder: Fernet = Fernet(config.secret.fernet_key)
    return decoder
