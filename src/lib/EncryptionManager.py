from . import FileCipher
#raplce above line with imports of the specific encryption class definitions
from . import Blowfish
from . import Constants as const
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
            self.fileCipher.decrypt(filePathStr, key)
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
            self.fileCipher = Blowfish.BLOWFISH
        
        print(f'Encryption algorithm {debug} selected.')

###########################################################################
    def checkSelectedFileEncryptionStatus(self, file : str) -> bool : 
        self.selectedFile = file
        self.fileIsEncrypted = (file[len(file) - 4 :] == const.ENCRYPTED_SUBSTRING)
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