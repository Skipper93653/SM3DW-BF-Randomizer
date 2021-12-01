import PyInstaller.__main__
import os

os.system('cmd /c "mkdir dist"')

os.system('cmd /c "copy ico.ico dist"')

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--icon=ico.ico'
])
