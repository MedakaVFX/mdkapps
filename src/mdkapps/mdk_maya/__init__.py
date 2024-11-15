""" mdk_maya
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2024-11-15 Tatsuya Yamagishi
        * added: path
"""

VERSION = 'v0.0.1'
NAME = 'mdk_maya'

import os
import sys


import maya.cmds as cmds
import maya.mel as mel


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_maya package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')



def clear_plugins():
    """ 不要なプラグインデータを削除 """
    print('MDK | [Clear Plugins]')

    plugs_ = cmds.unknownPlugin(q=True, list=True)

    if not plugs_ is None:
        plugs_.sort()

        for plug_ in plugs_:
            try:
                cmds.unknownPlugin(plug_, remove=True)
            except Exception as error:
                print('MDK | === error ===')
                print('type:' + str(type(error)))
                print('args:' + str(error.args))


    nodes_ = cmds.ls(type='unknown')
    if nodes_:
        for node_ in nodes_:
            try:
                cmds.delete(node_)
                print('//Delete unknownNode: ' + node_)

            except Exception as error:
                print('MDK | === error ===')
                print('type:' + str(type(error)))
                print('args:' + str(error.args))



def create_playblast(filepath: str, size: list|tuple=None, range: list|tuple=None):
    """ プレイブラストを作成
    
    Args:
        filepath(str): 出力ファイルパス
        size(list | turple): サイズ
        range(list | turple): サイズ
    """

    _FILE_FORMATS = {
        'jpg': 8,
        'png': 32,
    }
    
    _startframe, _endframe = range
    _extension = filepath.split('.')[-1] if '.' in filepath else ''
    cmds.setAttr ('defaultRenderGlobals.imageFormat', _FILE_FORMATS[_extension.lower()])

    

    cmds.playblast( 
            f=filepath,
            v=False,
            percent=100,
            format='image',
            widthHeight=size,
            startTime=_startframe,
            endTime=_endframe,
            forceOverwrite=False
        )