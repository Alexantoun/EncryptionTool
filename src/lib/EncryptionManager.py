from . import FileCipher
from . import Constants as const
from enum import Enum
import lib.KeyPrompts as KeyPrompts

class Algorithms_E(Enum):
    AES_CBC = 0
    B_FISH  = 1

RESPONSE_TYPE_OK = KeyPrompts.gtk.ResponseType.OK

###########################################################################
class Manager:
    def encryptClicked(self):
        print(f'\tEncrypting {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')
        prompt = KeyPrompts.EncryptionPrompt(self.mainWindow)
        
        response = prompt.run()
        if(response == RESPONSE_TYPE_OK):
            key = prompt.get_entry()
            print(f'The key entered is: {key}')
            filePathStr = f'{self.pathToFile}/{self.selectedFile}'        
            self.fileCipher.Encrypt(filePathStr, key)
        else:
            print('\tAbort encryption')

        prompt.destroy()

###########################################################################        
    def decryptClicked(self):
        print(f'\tDecrypting {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')
        prompt = KeyPrompts.DecryptionPrompt(self.mainWindow)
        
        response = prompt.run()
        if(response == RESPONSE_TYPE_OK):
            key = prompt.get_entry()
            print(f'The key entered is: {key}')
            filePathStr = f'{self.pathToFile}/{self.selectedFile}'        
            self.fileCipher.Decrypt(filePathStr, key)
        else:
            print('\tAbort decryption')

        prompt.destroy()

###########################################################################
    def setAlgorithm(self, algorithm : Algorithms_E):
        self.algorithm = algorithm
        debug : str

        if(Algorithms_E.AES_CBC == algorithm):
            debug = 'AES-CBC'
            self.fileCipher = FileCipher.AES_CBC
        elif(Algorithms_E.B_FISH == algorithm):
            debug = 'Blowfish'
            self.fileCipher = FileCipher.BLOWFISH_CBC
        
        print(f'Encryption algorithm {debug} selected.')

###########################################################################
    def checkSelectedFileEncryptionStatus(self, file : str) -> bool : 
        self.selectedFile = file
        self.fileIsEncrypted = (file[len(file) - 4 :] == const.ENCRYPTED_FILE_ENDING)
        print(f'File encryptor focusing on {self.pathToFile}/{self.selectedFile} : is encrypted = {self.fileIsEncrypted}')
        return self.fileIsEncrypted 

###########################################################################
    def onCipherButtonClick(self, selectedFile : str):
        self.selectedFile = selectedFile        
        print(f'Will operate on file {self.pathToFile}/{self.selectedFile}, with algorithm {self.algorithm}')

        if not self.fileIsEncrypted:
            self.encryptClicked()
        else:
            self.decryptClicked()

###########################################################################
    def __init__(self, mainWindow):
        self.selectedFile : str
        self.pathToFile : str
        self.algorithm : Algorithms_E
        self.fileCipher : FileCipher
        self.fileIsEncrypted : bool
        self.mainWindow = mainWindow