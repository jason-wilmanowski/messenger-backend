import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from messenger.core.config import Settings


settings = Settings()

class EncryptText:

    KEY = settings.MESSAGE_SECRET_KEY.encode()[:32]


    @staticmethod
    def encrypt(text : str):

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(EncryptText.KEY), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(text.encode()) + encryptor.finalize()
        return base64.b64encode(iv + ct).decode()


    @staticmethod
    def decrypt(cipher_text : str):
        data = base64.b64decode(cipher_text.encode())
        iv, ct = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(EncryptText.KEY), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return (decryptor.update(ct) + decryptor.finalize()).decode()
