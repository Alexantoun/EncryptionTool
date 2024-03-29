# from Crypto.Cipher import Blowfish

class FileCipher:
    def __init__(self):
        print("Created FileCipher")
    
    def encrypt(self, pathToFile : str , key : str):
        pass
    
    def Decrypt(self, pathToFile : str , key : str):
        print("BUILD THE DECRYPTION")

class Blowfish(FileCipher):
    def encrypt(self, pathToFile : str, key : str):
        print(f'Need to implement Blowfish.\n\tpathToFile = {pathToFile}.\n\tKey = {key}')

class RSA(FileCipher):
    def encrypt(self, pathToFile : str, key : str):
        print(f'Need to implement RSA.\n\tpathToFile = {pathToFile}.\n\tKey = {key}')

class AES_CBC(FileCipher):
    def encrypt(self, pathToFile : str, key : str):
        print(f'Need to implement AES_CBC.\n\tpathToFile = {pathToFile}.\n\tKey = {key}')
