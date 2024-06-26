from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from .. import Constants as const

BLOCK_SIZE = Blowfish.block_size

###########################################################################
def Encrypt(pathToFile : str, key : str):
    outputFile = pathToFile + const.ENCRYPTED_SUBSTRING
    key = key.encode('utf-8')
    print(f'Blowfish - Encrypting: \n\tpathToFile = {pathToFile}\n\tKey = {key}\n\tOutput file will be: {outputFile}')
    
    initVector = get_random_bytes(BLOCK_SIZE)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, initVector) #create new cipher object

    with open(pathToFile, 'rb') as file: #open file and read as binary
        fileData = file.read()
    
    paddedData = pad(fileData, BLOCK_SIZE) #Pad data until length is a multiple of block size
    encryptedData = cipher.encrypt(paddedData)

    with open(outputFile, 'wb') as encryptedFile:
        encryptedFile.write(initVector + encryptedData)

###########################################################################
def Decrypt(pathToFile : str, key : str):
    subStringCount = -len(const.ENCRYPTED_SUBSTRING)
    outputFile = pathToFile[:subStringCount]
    print(f'Blowfish - Decrypting : \n\tpathToFile = {pathToFile}\n\tKey = {key}\n\tOutput file will be: {outputFile}')

    key = key.encode('utf-8')

    with open(pathToFile, 'rb') as encryptedFile: #get encrypted files IV and get plain ol' data
        initVector = encryptedFile.read(BLOCK_SIZE)
        encryptedData = encryptedFile.read()
    
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, initVector) #Create new cipher object
    decryptedData = cipher.decrypt(encryptedData)
    
    #remove padding
    try:
        unpaddedData = unpad(decryptedData, BLOCK_SIZE)
    except ValueError:
        print('Incorrect decryption')
        return
    
    with open(outputFile, 'wb') as outf:
        outf.write(unpaddedData)