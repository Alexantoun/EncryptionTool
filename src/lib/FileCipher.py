from Crypto.Cipher import Blowfish

class FileCipher:
    def __init__(self):
        print("Created FileCipher")
    
    def Encrypt(self, pathToFile : str , key : str):
        pass
    
    def Decrypt(self, pathToFile : str , key : str):
        print("BUILD THE DECRYPTION")

class Blowfish(FileCipher):
    def Encrypt(self, pathToFile : str, key : str):
        print(f'Need to implement Blowfish.\tpathToFile = {pathToFile}.\n\tKey = {key}')

class RSA(FileCipher):
    def Encrypt(self, pathToFile : str, key : str):
        print(f'Need to implement RSA.\tpathToFile = {pathToFile}.\n\tKey = {key}')

class AES_CBC(FileCipher):
    def Encrypt(self, pathToFile : str, key : str):
        print(f'Need to implement AES_CBC.\tpathToFile = {pathToFile}.\n\tKey = {key}')
