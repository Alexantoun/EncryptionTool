from . import FileCipher
from enum import Enum
from . import PasswordPrompt

class Algorithms_E(Enum):
    RSA     = 0
    AES_CBC = 1
    B_FISH  = 2

RESPONSE_TYPE_OK = PasswordPrompt.gtk.ResponseType.OK

class Manager:
    def onEncryptClicked(self, selectedFile : str):
        self.selectedFile = selectedFile
        print(f'Will encrypt file {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')
        prompt = PasswordPrompt.PasswordPrompt(self.MainWindow)
        response = prompt.run()
        if(response == RESPONSE_TYPE_OK):
            key = prompt.get_entry()
            print(f'The key entered is: {key}')            
            self.fileCipher.encrypt(self.pathToFile, key)
        else:
            print('Abort encryption')

        prompt.destroy()
        
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
        self.deleteMe_alternateButtonColor = not self.deleteMe_alternateButtonColor
        return self.deleteMe_alternateButtonColor
        
    def __init__(self, mainWindow):
        self.selectedFile : str
        self.pathToFile : str
        self.algorithm : Algorithms_E
        self.fileCipher : FileCipher
        self.deleteMe_alternateButtonColor = False
        self.MainWindow = mainWindow