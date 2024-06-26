from .. import FileCipher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad

BLOCK_SIZE = AES.block_size

def Encrypt(pathToFile: str, key: str):
    key = key.encode('utf-f')