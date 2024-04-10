#! /usr/bin/python3

from . import FileCipher
from Crypto.Cipher import Blowfish
from Crypto.Cipher import get_random_bytes
import PasswordPromptBox

class Blowfish(FileCipher.FileCipher):
    def encrypt(self, pathToFile : str, key : str):
        print(f'Need to implement Blowfish.\n\tpathToFile = {pathToFile}.\n\tKey = {key}')
        
    def __init__(self):
        self.PasswordPrompt = ''

        