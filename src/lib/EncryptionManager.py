from . import FileCipher
from enum import Enum

class Algorithms_E(Enum):
    RSA     = 0
    AES_CBC = 1
    B_FISH  = 2

class Manager:
    def onEncryptClicked(self):
        print(f'Will encrypt file {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')
        self.fileCipher.encrypt(self.pathToFile, 'placeholder_key')

    def onDecryptClicked(self):
        print(f'Will decrypt file {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')

    def setAlgorithm(self, algorithm : Algorithms_E):
        self.algorithm = algorithm
        debug : str

        if(Algorithms_E.RSA == algorithm):
            debug = 'RSA'
            self.fileCipher = FileCipher.RSA()
        elif(Algorithms_E.AES_CBC == algorithm):
            debug = 'AES-CBC'
            self.fileCipher = FileCipher.AES_CBC()
        elif(Algorithms_E.B_FISH == algorithm):
            debug = 'Blowfish'
            self.fileCipher = FileCipher.Blowfish()
        
        print(f'Encryption algorithm {debug} selected.')

    def checkSelectedFileEncryptionStatus(self, file : str) -> bool : 
        self.file = file
        print(f'File encryptor focusing on {self.pathToFile}/{self.file}')
        return False
        
    def __init__(self):
        self.selectedFile : str
        self.pathToFile : str
        self.algorithm : Algorithms_E
        self.fileCipher : FileCipher
