NAME_INDEX = 0
SIZE_INDEX = 1
MODIFIED_INDEX = 2

# ERROR_ENCRYPT_CLICKED_WITHOUT_FILE_SELECTED = '<span foreground="#ff1a1a" weight="normal">No file was selected for encryption.</span>' 
ERROR_NO_INPUT_IN_SEARCH_BAR = '<span foreground="#ff1a1a" weight="normal">No text was entered to search for - Removing filter.</span>'

ENCRYPTION_PROMPT_TITLE = "Enter an encryption key"
DECRYPTION_PROMPT_TITLE = "Enter the decryption key"

def FOLDER_SELECTED(path:str) -> str:
    string = '<span foreground="#000000" weight="normal">Displaying content in '+path+'</span>'
    return string

def ERROR_INPUT_NOT_FOUND(input:str) -> str: #Pretty sure this is redundant now
    string = '<span foreground="red" weight="Bold">No text was entered to search for</span>'
    return string