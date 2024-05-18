# from Crypto.Cipher import Blowfish

class FileCipher:
    def __init__(self):
        print("Created FileCipher")
    
    def encrypt(self, filePath : str , key : str):
        pass
    
    def Decrypt(self, filePath : str , key : str):
        print("BUILD THE DECRYPTION")

class Blowfish(FileCipher):
    def encrypt(self, filePath : str, key : str):
        print(f'Need to implement Blowfish.\n\tFile Path = {filePath}.\n\tKey = {key}')

class RSA(FileCipher):
    def encrypt(self, filePath : str, key : str):
        print(f'Need to implement RSA.\n\tFile Path = {filePath}.\n\tKey = {key}')

class AES_CBC(FileCipher):
    def encrypt(self, filePath : str, key : str):
        print(f'Need to implement AES_CBC.\n\tFile Path = {filePath}.\n\tKey = {key}')
