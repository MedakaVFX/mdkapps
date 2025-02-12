""" mdk_max
 
* VFX用3dsMax互換パッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2024-11-15 Tatsuya Yamagishi
        * added: path
"""

VERSION = 'v0.0.1'
NAME = 'mdk_max'

import os
import sys


import pymxs

if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_max package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')


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

