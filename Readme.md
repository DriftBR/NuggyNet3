# NuggyNet!
An open-source web browser I made with ChatGPT because I was bored.

## Features:
- NuggyNet Web Browser
- Chirp Social integration

![image](https://github.com/user-attachments/assets/54dacba4-2c4f-4e7e-9f9e-86a58f4f0374)

## building?
have these py modules first:
`pip install pyinstaller PyQt5 PyQtWebEngine`

use Pyinstaller with the following cmd (make sure it's in the PATH system environment variable, replace <folder location> with folder location)
`pyinstaller --noconfirm --onefile --windowed --icon "<Folder_Location>\Source code\icon.ico" --add-data "<Folder_Location>\Source code\about.html;." --add-data "<Folder_Location>\Source code\help.chm;." --add-data "<Folder_Location>\Source code\nwin.html;."  "<Folder_Location>\Source code\NuggyNet.py"`

If you don't have PyInstaller in PATH, use this command instead (replace <username> with username>):
`C:\Users\<username>\AppData\Roaming\Python\Python312\Scripts\pyinstaller.exe --noconfirm --onefile --windowed --icon "<Folder_Location>\Source code\icon.ico" --add-data "<Folder_Location>\Source code\about.html;." --add-data "<Folder_Location>\Source code\help.chm;." --add-data "<Folder_Location>\Source code\nwin.html;."  "<Folder_Location>\Source code\NuggyNet.py"`
