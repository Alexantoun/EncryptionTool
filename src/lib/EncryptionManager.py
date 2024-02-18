from Crypto.Cipher import Blowfish

class EncryptionManager:
    def encryptButton(self):
        print(f'Will encrypt file {self.pathToFile}/{self.selectedFile}, with algorithm {self.selectedAlgorithm}')     

    def __init__(self):
        self.selectedFile : str
        self.pathToFile : str
        self.selectedAlgorithm : str