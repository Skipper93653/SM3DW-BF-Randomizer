import PyInstaller.__main__
import os, shutil

if not os.path.isdir('./dist'):
    os.mkdir('./dist')

shutil.copy2('./ico.ico', './dist')

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '-nrando',
    '--windowed',
    '--icon=ico.ico'
])
