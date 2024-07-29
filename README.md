AAA_EncryptionTool
This GUI-based encryption tool was made as a medium for Project-based learning in both Python and GTK. While I'm confident enough to use it for my own personal needs, I don't recommend using it for the encryption of critical files,
or any file that is considered important in any regard.

This software does not make backups of any encryption keys any user makes, and the user is solely responsible for their encryption/decryption keys. Additionally, users should also know which encryption algorithm was used to encrypt the file (either AES CBC or Blowfish CBC) for reliable decryption of files.

Disclaimer: The creator of this software is not responsible for any loss of data or access to files due to faulty software. Users are advised to use the software at their own risk and ensure they have proper backups of all important files and keys.

The AAA_EncryptionTool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AAA_EncryptionTool is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the combined license file that includes 
GNU General Public License and Simplified BSD License
along with AAA_EncryptionTool  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2024 Alexander Andrew Antoun

### Getting Started
1. **Usage:**
    - **Encrypt Files** 
        - Use the "Open" button to open an explorer and navigate to the location of the file to encrypt. Click on "Select Folder" in the upper right-hand corner of the explorer window.
        - Files in the chosen folder will appear in the list view. Select the file you wish to encrypt, or you can search for the file name at the top of the application window.
        - Use the radio buttons above the list view to **select which encryption algorithm you wish to use**.
        - If the file selected is unencrypted, click the encrypt button to open up the password prompts.
        - Enter the encryption key you wish to use. **Keys that are too short for AES will be padded with null characters** and click OK.
        - Clicking Refresh at the top of the application window will show an additional .enc file in the list view. This is the encrypted copy of the file.
        
    - **Decrypt Files**
        - Use the "Open" button to open an explorer and navigate to the location of the file to decrypt. Click on "Select Folder" in the upper right-hand corner of the explorer window.
        - Files in the chosen folder will appear in the list view. Select the file you wish to decrypt, or you can search for the file name at the top of the application window.
        - Use the radio buttons above the list view to **select which encryption algorithm was used** to encrypt the file.
        - If the file selected is encrypted, click the decrypt button to open up the password prompts.
        - Enter the decryption key. **Keys that are too short for AES will be padded with null characters**.
        - Click OK to decrypt the file.
        - Clicking Refresh at the top of the application window will show an additional file without the .enc postfix in the list view. This is the decrypted copy of the file.

    - **Backup Your Keys**
        - This software does not make backups of encryption keys used, nor backups of files encrypted. The original file you encrypt should be backed up securely.

    - **Overwriting Files**
        - Should you encrypt a file, then decrypt the encrypted file in the same directory, **the original file will be overwritten**. While the contents should be the same, no guarantee is being given.