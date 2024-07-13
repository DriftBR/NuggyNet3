# NuggyNet!
an open-source (obviously) web browser I own! idk what else to say here other than if you install with installer, you get a source code folder with stuff you can use for modding


## building?
have these py modules first:
`pip install pyinstaller PyQt5 PyQtWebEngine`

use Pyinstaller with the following cmd (make sure it's in the PATH system environment variable, replace <folder location> with folder location)
`pyinstaller --noconfirm --onefile --console --icon "<folder location>\Source (for modders)\NN.ico" --add-data "<folder location>Source (for modders)\Homepage.html;." --add-data "<folder location>\Source (for modders)\NN.ico;." --add-data "<folder location>\Source (for modders)\NuggyNetMain.py;." --add-data "<folder location>\Source (for modders)\W95FA.otf;."  "<folder location>\Source (for modders)\NuggyNetMain.py"`

If you don't have PyInstaller in PATH, use this command instead (replace <username> with username>):
`C:\Users\<username>\AppData\Roaming\Python\Python312\Scripts\pyinstaller.exe --noconfirm --onefile --console --icon "<folder location>\Source (for modders)\NN.ico" --add-data "<folder location>Source (for modders)\Homepage.html;." --add-data "<folder location>\Source (for modders)\NN.ico;." --add-data "<folder location>\Source (for modders)\NuggyNetMain.py;." --add-data "<folder location>\Source (for modders)\W95FA.otf;."  "<folder location>\Source (for modders)\NuggyNetMain.py"`

anyways,

Things I'd like:
|_ Different web engine (that isn't chromium)
|_ New web render engine (which renders HTML buttons/textboxes as native windows buttons)
|_ A settings menu (previous one quite literally bluescreened my PC)
|_ A settings.ini file to go with settings)

# stuff that exists
[x] cool 90s theme
[x] menu bar (press alt)
[ ] settings menu
[ ] new web engine

[Original NuggyNet Repo](https://www.github.com/Kirb101/NuggetWeb) | [My BORING website](https://awethebird.neocities.org) | [Main YouTube channel](https://www.youtube.com/@nuggetbirb) | [Second channel](https://www.youtube.com/@nuggetbirbcult)
