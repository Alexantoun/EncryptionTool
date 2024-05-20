from . import FileCipher
from enum import Enum
import lib.EncryptionPrompt as EncryptionPrompt
import lib.DecryptionPrompt as DecryptionPrompt

class Algorithms_E(Enum):
    RSA     = 0
    AES_CBC = 1
    B_FISH  = 2

RESPONSE_TYPE_OK = EncryptionPrompt.gtk.ResponseType.OK

###########################################################################
class Manager:
    def encryptClicked(self):
        print(f'\tEncrypting {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')
        prompt = EncryptionPrompt.EncryptionPrompt(self.mainWindow)
        
        response = prompt.run()
        if(response == RESPONSE_TYPE_OK):
            key = prompt.get_entry()
            print(f'The key entered is: {key}')
            filePathStr = f'{self.pathToFile}/{self.selectedFile}'        
            self.fileCipher.encrypt(filePathStr, key)
        else:
            print('\tAbort encryption')

        prompt.destroy()

###########################################################################        
    def decryptClicked(self):
        print(f'\tDecrypting {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')
        prompt = DecryptionPrompt.DecryptionPrompt(self.mainWindow)
        
        response = prompt.run()
        if(response == RESPONSE_TYPE_OK):
            key = prompt.get_entry()
            print(f'The key entered is: {key}')
            filePathStr = f'{self.pathToFile}/{self.selectedFile}'        
            self.fileCipher.encrypt(filePathStr, key)
        else:
            print('\tAbort decryption')

        prompt.destroy()

###########################################################################
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

###########################################################################
    def checkSelectedFileEncryptionStatus(self, file : str) -> bool : 
        self.selectedFile = file
        print(f'File encryptor focusing on {self.pathToFile}/{self.selectedFile}')
        self.deleteMe_alternateButtonColor = not self.deleteMe_alternateButtonColor
        return self.deleteMe_alternateButtonColor

###########################################################################
    def onCipherButtonClick(self, selectedFile : str):
        self.selectedFile = selectedFile        
        print(f'Will operate on file {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')

        if self.deleteMe_alternateButtonColor:
            self.encryptClicked()
        else:
            self.decryptClicked()

###########################################################################
    def __init__(self, mainWindow):
        self.selectedFile : str
        self.pathToFile : str
        self.algorithm : Algorithms_E
        self.fileCipher : FileCipher
        self.deleteMe_alternateButtonColor = False
        self.mainWindow = mainWindow