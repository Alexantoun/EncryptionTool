pyinstaller --onefile --name EncryptionTool \
    --add-data "src/forms/MainWindow.glade:forms" \
    --add-data "src/lib:lib" \
    --hidden-import=Crypto \
    --hidden-import=Crypto.Cipher \
    --hidden-import=Crypto.Cipher.Blowfish \
    --hidden-import=Crypto.Cipher.AES \
    --hidden-import=Crypto.Random \
    --hidden-import=Crypto.Util \
    --hidden-import=Crypto.Util.Padding \
    main.py
