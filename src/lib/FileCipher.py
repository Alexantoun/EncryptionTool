
from .EncryptionMethods import Blowfish
from .EncryptionMethods import AES

class FileCipher:
    def __init__(self):
        print("Created FileCipher")
    
    def Encrypt(pathToFile : str , key : str):
        pass
    
    def Decrypt(pathToFile : str , key : str):
        print("BUILD THE DECRYPTION")

###########################################################################
class RSA(FileCipher):
    def encrypt(pathToFile : str, key : str):
        print(f'Need to implement RSA.\n\tpathToFile = {pathToFile}.\n\tKey = {key}')

###########################################################################
class AES_CBC(FileCipher):
    def Encrypt(pathToFile : str, key : str):
        AES.Encrypt(pathToFile, key)
    
    def Decrypt(pathToFile : str, key : str):
        AES.Decrypt(pathToFile, key)

###########################################################################
class BLOWFISH_CBC(FileCipher):
    def Encrypt(pathToFile: str, key: str):
        Blowfish.Encrypt(pathToFile, key)
    
    def Decrypt(pathToFile : str, key : str):
        Blowfish.Decrypt(pathToFile, key)