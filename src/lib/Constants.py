NAME_INDEX = 0
SIZE_INDEX = 1
MODIFIED_INDEX = 2

ENCRYPTION_PROMPT_TITLE = "Enter an encryption key"
DECRYPTION_PROMPT_TITLE = "Enter the decryption key"

def FOLDER_SELECTED(path:str) -> str:
    string = '<span foreground="#000000" weight="normal">Displaying content in '+path+'</span>'
    return string

ENCRYPTED_FILE_ENDING = '.enc'