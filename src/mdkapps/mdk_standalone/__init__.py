""" mdk_standalone
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya Yamagishi
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2025-01-09 Tatsuya Yamagishi
"""

VERSION = 'v0.0.1'
NAME = 'mdk_standalone'

import os
import pathlib
import sys


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_standalone package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')

# ======================================= #
# Settings
# ======================================= #
EXT_LIST = [
    '.dat',
    '.txt',
]

EXT_DICT = {
    'asset': '.dat',
    'shot': '.txt',
    'geo': '.abc',
    'usd': '.usd',
}

# ======================================= #
# Functions
# ======================================= #
def create_playblast(filepath: str, size: list|tuple=None, range: list|tuple=None):
    """ プレイブラストを作成
    
    Args:
        filepath(str): 出力ファイルパス
        size(list | turple): サイズ
        range(list | turple): サイズ
    """

    print(f'MDK | {filepath=}')
    print(f'MDK | {size=}')
    print(f'MDK | {range=}')


# ======================================= #
# Class
# ======================================= #
class AppMain:
    def __init__(self):
        pass

    # --------------------------------- #
    # Get / Set
    # --------------------------------- #
    def get_ext(self, key: str) -> str:
        """ 拡張子を返す 
        
        """
        if key is None:
            return '.txt'
        
        if type(key) is not str:
            raise TypeError('key is not str.')


        return EXT_DICT.get(key.lower())
    

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    
    def get_filepath(self) -> str:
        """現在開いているファイルパスを取得"""
        return None
    
    # --------------------------------- #
    # I/O
    # --------------------------------- #
    def save_file(self, filepath):
        _file = pathlib.Path(filepath)
        # _file.parent.mkdir(parents=True, exist_ok=True)
        _file.write_text('Medaka', encoding='utf8')