""" mdk_nuke
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2024-11-15 Tatsuya Yamagishi
        * added: new
"""

VERSION = 'v0.0.1'
NAME = 'mdk_nuke'

import os
import sys

import nuke
import nukescripts

from PySide2 import QtWidgets

if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_nuke package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')

# ======================================= #
# Settings
# ======================================= #
EXT = '.nk'

EXT_LIST = [
    '.nk',
]

EXT_DICT = {
    'asset': '.nk',
    'shot': '.txt',
    'geo': '.abc',
    'usd': '.usd',
}

FILE_NODES_LIST = ['Read', 'Write', 'ReadGeo2', ]


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

    # --------------------------------- #
    # Get / Set
    # --------------------------------- #
    def get_ext(self, key: str = None) -> str:
        """ 拡張子を返す 
        
        """
        return EXT
    

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    
    def get_filepath(self) -> str:
        """現在開いているファイルパスを取得"""
        return nuke.root().name()
    

    def get_main_window(self):
        """ Get the Nuke main window.

        Reference from:
            * https://russell-vfx.com/blog/2020/8/20/main-window
            * https://gist.github.com/paulwinex/b00fcff40ee8392d3220990b358d9337
    
        Returns:
            PySide2.QtWidgets.QWidget: 'QWidget' Nuke main window.
        """
        # for _widget in QtWidgets.QApplication.topLevelWidgets():
        #     if _widget.metaObject().className() == 'Foundry::UI::DockMainWindow':
        #         return _widget
            
        #     raise RuntimeError('Could not find DockMainWindow instance')

        return QtWidgets.QApplication.activeWindow()

    
    # --------------------------------- #
    # I/O
    # --------------------------------- #
    def import_file(self, filepath: str):
        """ ファイルの読み込み
        
        """
        if type(filepath) == str:
        
            nuke.tcl('drop', filepath)
            result = nuke.selectedNodes()

            # 読み込み時のノードクラス毎の処理
            # nodes = nuke.selectedNodes('Read')
            # if nodes:
            #     for node in nodes:
            #         node['raw'].setValue(True)
            #         node.autoplace()

            return result

        else:
            raise TypeError('"Filepath" type is not str')


    def import_files(self, filepath_list: list[str]):
        for _filepath in filepath_list:
            self.import_file(_filepath)


    def open_dir(self):
        """ 選択しているノードのファイルパスのディレクトリを開く
         
        """
        nodes = nuke.selectedNodes()

        if len(nodes)==0:
            filepath = nuke.root().name()
            print(f'file = {filepath}')

            if os.path.exists(filepath):
                # dirpath = os.path.dirname(path)
                self.core.open_in_explorer(filepath)

        else:
            for node in nuke.selectedNodes():
                nodeclass = node.Class()
            
                if nodeclass in FILE_NODES_LIST:
                    filepath = os.path.dirname(nuke.filename(node))
                    print(f'file = {filepath}')

                    self.core.open_in_explorer(filepath)


    def open_file(self, filepath):
        """ Plugin Builtin Function """
        self.file.open_file(self, filepath)


    def save(self):
        """ Plugin Builtin Function
        * 上書き保存
        """
        self.file.save()


    def save_file(self, filepath, mkdir=False):
        """ ファイル保存 """
        if mkdir:
            _dirpath = os.path.dirname(filepath)
            if not os.path.exists(_dirpath):
                os.makedirs(_dirpath)

        nuke.scriptSaveAs(filepath, -1)