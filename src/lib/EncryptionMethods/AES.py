from .. import Constants as const
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad

BLOCK_SIZE = AES.block_size
MAX_KEY_LENGTH_b = 32
KEY_LENGTHS_b = [16, 24, 32]

###########################################################################
def PadKey(key : str) -> str:
    targetLength = next(length for length in KEY_LENGTHS_b if (len(key) <= length))
    return key.ljust(targetLength, b'\0')

###########################################################################
def Encrypt(pathToFile: str, key: str):
    outputFile = pathToFile + const.ENCRYPTED_FILE_ENDING
    key = key.encode('utf-8')

    keyLength = len(key)
    if keyLength > MAX_KEY_LENGTH_b:
        print(f'Invalid key length: {keyLength}')
        return
    
    paddedKey = PadKey(key)
    print(f'AES - Encrypting: \n\tpathToFile = {pathToFile}\n\tOutput file will be: {outputFile}')

    with open(pathToFile, 'rb') as file:
        fileData = file.read()
        
    initVector = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(paddedKey, AES.MODE_CBC, initVector)
    paddedData = pad(fileData, BLOCK_SIZE)
    encryptedData = cipher.encrypt(paddedData)
    
    with open(outputFile, 'wb') as encryptedFile:
        encryptedFile.write(initVector + encryptedData)

###########################################################################
def Decrypt(pathToFile : str, key : str):
    substringCount = -len(const.ENCRYPTED_FILE_ENDING)
    outputFile = pathToFile[:substringCount]
    print(f'AES - Decrypting : \n\tpathToFile = {pathToFile}\n\tOutput file will be: {outputFile}')

    key = key.encode('utf-8')
    paddedKey = PadKey(key)

    with open(pathToFile, 'rb') as encryptedFile: #get encrypted files IV and get plain ol' data
        initVector = encryptedFile.read(BLOCK_SIZE)
        encryptedData = encryptedFile.read()
    
    cipher = AES.new(paddedKey, AES.MODE_CBC, initVector)
    decryptedData = cipher.decrypt(encryptedData)

    try:
        unpaddedData = unpad(decryptedData, BLOCK_SIZE)
    except ValueError:
        print('Incorrect decryption')
        return
    
    with open(outputFile, 'wb') as outf:
        outf.write(unpaddedData)