import os

cwdir: str = ''

def current_wdir():
    return f'{os.getcwd()}\{cwdir}\\'

def assets_dir():
    return f'{current_wdir()}assets'

def icons_dir():
    return f'{assets_dir()}\icons'

def windows_dir():
    return f'{current_wdir()}windows'