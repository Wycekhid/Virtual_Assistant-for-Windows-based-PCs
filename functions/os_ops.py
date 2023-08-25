import os
import subprocess as sp

paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'need for speed': "C:\\Users\\Lesley\\OneDrive\\Desktop\\Need for Speed Most Wanted Limited Edition.lnk",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'pycharm': "C:\\Users\Public\\Desktop\\PyCharm Community Edition 2023.1.2.lnk"
}


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_notepad():
    os.startfile(paths['notepad'])


def open_cmd():
    os.system('start cmd')


def open_calculator():
    sp.Popen(paths['calculator'])


def open_nfs():
    os.startfile(paths['need for speed'])


def open_pycharm():
    os.startfile(paths['pycharm'])
