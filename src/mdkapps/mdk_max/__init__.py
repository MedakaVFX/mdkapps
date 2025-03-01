""" mdk_max
 
* VFX用3dsMax互換パッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.2 (v0.0.2) 2025-02-12 Tatsuya Yamagishi
    * v0.0.1 (v0.0.1) 2024-11-15 Tatsuya Yamagishi
        * added: path
"""

VERSION = 'v0.0.2'
NAME = 'mdk_max'

import os
import sys

import pymxs
rt = pymxs.runtime

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except:
    from qtpy import QtCore, QtGui, QtWidgets


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_max package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')

#=======================================#
# Max Settings
#=======================================#
EXT_LIST = [
    '.max',
    '.abc',
    '.fbx',
    '.obj',
    '.usd',
]


#=======================================#
# Functions
#=======================================#
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


    def get_ext(self) -> str:
        """ 拡張子を返す 
        
        """
        return '.max'
    

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    

    def get_framerange(self) -> tuple[int]:
        _start_frame = rt.animationRange.start
        _end_frame = rt.animationRange.end

        return _start_frame, _start_frame, _end_frame, _end_frame


    def get_main_menubar(self) -> QtWidgets.QMenu:
        _main_window = self.get_main_window()

        if _main_window is not None:
            return _main_window.menuBar()
        
        else:
            raise RuntimeError('Could not find main window.')


    def get_main_window(self):
        """Get the 3DS MAX main window.
        
        Returns:
            PySide2.QtWidgets.QMainWindow: 'QMainWindow' 3DS MAX main window.


        Reference:
            * https://russell-vfx.com/blog/2020/8/20/main-window
        """
        for _widget in QtWidgets.QApplication.instance().topLevelWidgets():
            if isinstance(_widget, QtWidgets.QMainWindow) and "Autodesk" in _widget.windowTitle():
                return _widget
        return None
    

    def import_file(self, filepath: str, namespace=None):
        """ ファイルをインポート
        """
        rt.importFile(filepath)


    def import_files(self, filepath_list: list[str], namespace=None):
        for _filepath in filepath_list:
            self.import_file(_filepath, namespace=namespace)
