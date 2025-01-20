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

#=======================================#
# Import Built-in
#=======================================#
import os
import re
import sys

#=======================================#
# Import Maya Modules
#=======================================#
import maya.cmds as cmds
import maya.mel as mel

import mayaUsd.ufe
import mayaUsd.lib
import mayaUsd_createStageWithNewLayer

import ufe


#=======================================#
# Settings
#=======================================#
if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_maya package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')

#=======================================#
# Settings
#=======================================#
EXT_LIST = [
    '.mb',
    '.ma',
    '.abc',
    '.fbx',
    '.obj',
]

EXT_DICT = {
    'asset': '.txt',
    'geo': '.abc',
    'usd': '.usd',
}

FILE_FILTER_SCRIPT = re.compile(r'.+\.(py)')


#=======================================#
# Functions
#=======================================#
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



def create_playblast(filepath: str, size: list|tuple=None, range: list|tuple=None, filetype='jpg'):
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
    cmds.setAttr ('defaultRenderGlobals.imageFormat', _FILE_FORMATS[filetype])

    

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
    

def exec_script(filepath):
    if FILE_FILTER_SCRIPT.match(filepath):
        if filepath.lower().endswith('.py'):
            exec_python_file(filepath, globals())
    else:
        raise TypeError()
    

def exec_python_file(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        '__file__': filepath,
        '__name__': '__main__',
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)



# ======================================= #
# Class
# ======================================= #
class AppMain:
    def __init__(self):
        pass

    def add_recent_file(self, filepath: str):
        filepath = filepath.replace('\\','/') 
        _filename, _ext = os.path.splitext(filepath)
        _ext = _ext.lower()

        if _ext == '.ma':
            cmd = 'addRecentFile( "{}", "mayaAscii")'.format(filepath)
            mel.eval(cmd)
        elif _ext == '.mb':
            cmd = 'addRecentFile( "{}", "mayaBinary")'.format(filepath)
            mel.eval(cmd)

    def get_all_lights(self) -> list[str]:
        """
        typeList = [
            'aiSkyDomeLight',
            'VRayLightRectShape'
        ]
        
        allLights = cmds.ls(lights=True)
        allLights.extend(cmds.ls(type=typeList))
        
        """
        _exclude_classifications = 'light/vloume:light/filter:hidden'
        _type_list = cmds.listNodeTypes('light', exclude=_exclude_classifications)
        
        return cmds.ls(type=_type_list)


    def get_current_render(self) -> str:
        return cmds.getAttr('defaultRenderGlobals.currentRenderer')

    def get_ext(self, key: str = None) -> str:
        """ 拡張子を返す 
        
        """
        if key is None:
            return '.mb'
        
        else:
            return EXT_DICT.get(key)
            

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    

    def get_filepath(self) -> str:
        return cmds.file(q=True, sceneName=True)
    

    def get_main_window(self):
        ptr = omui.MQtUtil.mainWindow()

        if ptr is not None:
            return wrapInstance(int(ptr), QtWidgets.QWidget)
        

    def save_file(self, filepath: str, mkdir=False, recent=False):
        """ ファイル保存 """
        if mkdir:
            _dirpath = os.path.dirname(filepath)
            if not os.path.exists(_dirpath):
                os.makedirs(_dirpath)


        if recent:
            self.add_recent_file(filepath)


        cmds.file(rename=filepath)

        filename, ext = os.path.splitext(filepath)
        if ext.lower() == '.mb':
            cmds.file(save=True, type='mayaBinary')
        elif ext.lower() == '.ma':
            cmds.file(save=True, type='mayaAscii')


    def save_selection(self, filepath: str):
        """ 選択を保存 """
        filetype_dict = {
            '.mb': 'mayaBinary',
            '.ma': 'mayaAscii',
            '.fbx': 'FBX export',
        }

        _nodes = cmds.ls(sl=True)
        if not _nodes:
            RuntimeError('TY | Select any node')

        _, _ext = os.path.splitext(filepath)
        _ext = _ext.lower()
        _filetype = filetype_dict.get(_ext)
        cmds.file(filepath, force=True, type =_filetype, exportSelected=True)