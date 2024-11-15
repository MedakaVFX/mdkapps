""" mdk_standalone
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2024-11-15 Tatsuya Yamagishi
"""

VERSION = 'v0.0.1'
NAME = 'mdk_standalone'

import os
import sys


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_standalone package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')



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