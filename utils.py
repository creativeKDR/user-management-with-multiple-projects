import uuid
import base64
from Cryptodome.Cipher import AES
from fastapi import HTTPException
from schemas import project_source

from config import Config as config


class Utilities:

    @staticmethod
    def generateID():
        # generate unique document IDs
        return uuid.uuid4()

    @staticmethod
    def check_model_source(source):
        if source not in project_source:
            # checking if model type is available or not
            raise HTTPException(status_code=400, detail="Unsupported source")
        return project_source.get(source)


BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s: s[0:-ord(s[-1:])]


class AESCipher:

    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.iv = iv

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = cipher.encrypt(raw)
        encrypted_data = base64.b64encode(enc)
        return encrypted_data

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_data = unpad(cipher.decrypt(enc)).decode('utf-8')
        return decrypted_data


cipher = AESCipher(config.aes_key, config.aes_iv)
