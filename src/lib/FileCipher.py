
from .EncryptionMethods import Blowfish
from .EncryptionMethods import AES

class FileCipher:
    def __init__(self):
        print("Created FileCipher")
    
    def Encrypt(pathToFile : str , key : str):
        pass
    
    def Decrypt(pathToFile : str , key : str):
        pass

###########################################################################
class AES_CBC(FileCipher):
    @staticmethod
    def Encrypt(pathToFile : str, key : str):
        AES.Encrypt(pathToFile, key)
    
    @staticmethod
    def Decrypt(pathToFile : str, key : str):
        AES.Decrypt(pathToFile, key)

###########################################################################
class BLOWFISH_CBC(FileCipher):
    @staticmethod
    def Encrypt(pathToFile: str, key: str):
        Blowfish.Encrypt(pathToFile, key)
    
    @staticmethod
    def Decrypt(pathToFile : str, key : str):
        Blowfish.Decrypt(pathToFile, key)