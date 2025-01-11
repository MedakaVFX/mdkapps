""" mdk_houdini
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2025-01-08 Tatsuya Yamagishi
"""

VERSION = 'v0.0.1'
NAME = 'mdk_houdini'

import os
import sys

import hou


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_houdini package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')

# ======================================= #
# Settings
# ======================================= #
EXT = {
    'hindie': '.hiplc',
}

EXT_LIST = [
    '.abc',
    '.hip',
    '.hiplc',
    '.bgeo',
]

EXT_DICT = {
    'asset': '.dat',
    'shot': '.txt',
    'geo': '.abc',
    'usd': '.usd',
}

# ======================================= #
# Functins
# ======================================= #
def create_playblast(filepath: str, size: list|tuple=None, range: list|tuple=None, filetype='jpg'):
    """ プレイブラストを作成
    
    Args:
        filepath(str): 出力ファイルパス
        size(list | turple): サイズ
        range(list | turple): サイズ
    """

    raise RuntimeError('未実装')


# ======================================= #
# Class
# ======================================= #
class AppMain:
    def __init__(self):
        pass


    def get_ext(self, key: str) -> str:
        """ 拡張子を返す 
        
        """
        _mode = hou.applicationName()
        _ext = EXT.get(_mode)

        if _ext:
            return _ext
        else:
            return '.hip'
            

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    

    def get_filepath(self) -> str:
        hou.hipFile.path()
    

    def get_main_window(self):
        """ Get the Houdini main window.

        * Reference from: https://russell-vfx.com/blog/2020/8/20/main-window
    
        Returns:
            PySide2.QtWidgets.QWidget: 'QWidget' Houdini main window.
        """
        return hou.qt.mainWindow()
    

    def save_file(self, filepath):
        """ Plugin Builtin Function
        
        * 名前を付けて保存

        """
        hou.hipFile.save(file_name=filepath, save_to_recent_files=True)