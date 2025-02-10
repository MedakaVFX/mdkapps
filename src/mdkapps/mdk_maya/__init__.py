""" mdk_maya
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.3 (v0.0.3) 2025-02-07 Tatsuya Yamagishi
        * added : apply_alembic_cache()

    * v0.0.2 (v0.0.2) 2025-02-03 Tatsuya Yamagishi
        * fixed : export_nodes()
        * upateed : ファイル判定関数

    * v0.0.1 (v0.0.1) 2025-01-31 Tatsuya Yamagishi
        * New
"""

VERSION = 'v0.0.3'
NAME = 'mdk_maya'

#=======================================#
# Import Built-in
#=======================================#
import os
import pathlib
import platform
import re
import subprocess
import sys

#=======================================#
# Import Maya Modules
#=======================================#
import maya.cmds as cmds
import maya.mel as mel

import mayaUsd.ufe
import mayaUsd.lib
import mayaUsd_createStageWithNewLayer

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except:
    from qtpy import QtCore, QtGui, QtWidgets

from maya import OpenMayaUI as omui 

try:
    from shiboken2 import wrapInstance
except:
    from shiboken6 import wrapInstance

import ufe


#=======================================#
# Modlue Settings
#=======================================#
if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_maya package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')


#=======================================#
# MayaSettings
#=======================================#
ATTR_LIST = ('tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz')

EXT_LIST = [
    '.mb',
    '.ma',
    '.abc',
    '.fbx',
    '.obj',
    '.usd',
]

EXT_DICT = {
    'asset': '.mb',
    'geo': '.abc',
    'shot': '.ma',
    'usd': '.usd',
}

FILE_FILTER_ABC = re.compile(r'.+\.(abc)')
FILE_FILTER_FBX = re.compile(r'.+\.(fbx)')
FILE_FILTER_USD = re.compile(r'.+\.(usd|usdc|usda)')
FILE_FILTER_IMAGE = re.compile(r'.+\.(png|jpeg|jpg|tif|tiff|exr|tx|hdr)')
FILE_FILTER_IMAGE_SDR = re.compile(r'.+\.(bmp|gif|png|jpeg|jpg|svg|tif|tiff)')
FILE_FILTER_MAYA = re.compile(r'.+\.(ma|mb|abc|fbx|obj)')
FILE_FILTER_MEDIA = re.compile(r'.+\.(bmp|png|jpeg|jpg|svg|tif|tiff|exr|mp4|mp3|pdf|mov|mkv)')
FILE_FILTER_OBJ = re.compile(r'.+\.(obj)')
FILE_FILTER_RAW = re.compile(r'.+\.(cr2|cr3|dng|CR2|CR3|DNG)')
FILE_FILTER_SCRIPT = re.compile(r'.+\.(py)')
FILE_FILTER_TEXT = re.compile(r'.+\.(doc|txt|text|json|py|usda|nk|sh|zsh|bat)')


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


def open_in_explorer(filepath: str):
    """
    Explorerでフォルダを開く
    """
    if os.path.exists(filepath):
        if platform.system() == 'Windows':
            filepath = str(filepath)
            filepath = filepath.replace('/', '\\')

            filebrowser = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
            subprocess.run([filebrowser, '/select,', os.path.normpath(filepath)])
        
        elif platform.system() == 'Darwin':
            subprocess.call(['open', filepath])
        
        else:
            subprocess.Popen(["xdg-open", filepath])
    else:
        raise FileNotFoundError(f'File is not found.')


# ======================================= #
# Class
# ======================================= #
class AppMain:
    def __init__(self):
        pass

    def apply_alembic_cache(self, filepath: str):
        # 選択しているオブジェクトを取得
        _selection = cmds.ls(sl=True)
        
        if not _selection:
            cmds.warning("オブジェクトを選択してください。")
            return
        
        # for _obj in _selection:
        #     _shape = cmds.listRelatives(_obj, shapes=True)
        #     if not _shape:
        #         cmds.warning(f"{_obj} have not shape node.")
        #         continue
            
        #     _shape = _shape[0]
            
        # Alembicキャッシュを適用
        print(f'Apply Alembic Cache: {filepath}')
        cmds.AbcImport(filepath, mode="import", connect=_selection[0])
        # cmds.AbcImport(filepath, mode="import", rpr=_selection[0], merge=True)


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


    def create_playblast(
                self,
                filepath: str,
                name: str,
                size: list|tuple=None,
                framerange: list|tuple=None,
                ext: str = '.jpg',):
        
        """
        * defaultRenderGlobals.imageFormat
        """

        _file_format_dict = {
            '.jpg': 8,
            '.png:': 32,
        }
        
        print('# --------------------------------- #')
        print('# Create Playblast')
        print('# --------------------------------- #')

        print(f'Name: {name}')
        print(f'Size: {size}')
        print(f'Ext: {ext}')
        print(f'Range: {framerange}')
        print(f'Filepath: {filepath}')

        
        cmds.setAttr(
                'defaultRenderGlobals.imageFormat',
                _file_format_dict[ext]
        )

        cmds.playblast( 
            f = f'{filepath}/{name}',
            v = False, 
            percent = 100,
            format = 'image',
            widthHeight = size,
            startTime = framerange[0],
            endTime = framerange[1],
            forceOverwrite = True,
        )


    def export_abc(
                self,
                filepath: str,
                nodes: list[str],
                startframe: int = None,
                endframe: int = None):
        
        """
        Reference from:

            - https://stackoverflow.com/questions/43612557/maya-abcexport-with-python

        """
        if not nodes:
            raise ValueError('Select any nodes')
        
        cmds.select(nodes)
        if (startframe is None) and (endframe is None):
            frames = ''

        else:
            frames = f'-frameRange {startframe} {endframe}'

        if nodes and cmds.nodeType(nodes[0]) == "transform":
            name = nodes[0]
            if name.find("|")!= -1:
                name = name.rsplit("|",1)[1]

            nodes = "".join([" -root "+x for x in nodes])
            mel_cmd = f'AbcExport -j "{frames} -stripNamespaces -uvWrite{nodes} -file {filepath}"'

            # Make directory
            dirname = os.path.dirname(filepath)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            
            try:
                mel.eval(mel_cmd)
            except Exception as ex:
                raise ValueError (ex)


    def export_fbx(
                self,
                filepath: str,
                nodes: list[str],
                startframe=None,
                endframe=None):
        
        """
        Reference From:

            - https://forums.autodesk.com/t5/maya-animation-and-rigging/export-animation-with-specific-frame-range-in-python/td-p/8945591

        Examples:
            >>> mel.eval('FBXResetExport;')
            >>> mel.eval('FBXExportBakeComplexAnimation -v true;')
            >>> mel.eval('FBXExportEmbeddedTextures -v false;')
            >>> mel.eval("FBXExportSplitAnimationIntoTakes -clear;")
            >>> # Up Axis
            >>> mel.eval("FBXExportUpAxis z;")
            >>> # Export Animation from frame x to frame y
            >>> mel.eval('FBXExportSplitAnimationIntoTakes -v \"tata\" %d %d'%(int(startTime), int(endTime)))
            >>> mel.eval('FBXExport -f "%s" -s'%(fullName ) ) 
        
        """

        if not nodes:
            raise ValueError('Select any nodes')
            
        mel.eval('FBXResetExport;')
        # mel.eval('FBXExportEmbeddedTextures -v false;')

        if (startframe is not None) and (endframe is not None):
            mel.eval('FBXExportBakeComplexAnimation -v true;')    
            mel.eval("FBXExportSplitAnimationIntoTakes -clear;")
            mel.eval(f'FBXExportSplitAnimationIntoTakes -v \"tata\" {startframe} {endframe}')


        mel_cmd = f'FBXExport -f "{filepath}" -s'
        mel.eval(mel_cmd)

            
    def export_nodes(
                    self,
                    filepath: str,
                    nodes: list[str],
                    startframe=None,
                    endframe=None):
        
        if self.is_abc(filepath):
            self.export_abc(filepath, nodes, startframe, endframe)
        elif self.is_fbx(filepath):
            self.export_fbx(filepath, nodes, startframe, endframe)
        elif self.is_obj(filepath):
            self.save_selection(filepath, nodes, startframe, endframe)
        elif self.is_maya(filepath):
            cmds.select(nodes)
            self.save_selection(filepath)
        else:
            raise TypeError('MDK | Not supported file type')


    def export_usd(
                self,
                filepath: str,
                nodes: list[str],
                startframe=None,
                endframe=None):
        
        """ Export USD Selection

        * Reference from:
            - https://zenn.dev/remiria/articles/9ac3e31df4da98ba2f0b
            - https://github.com/Autodesk/maya-usd/blob/dev/lib/mayaUsd/commands/Readme.md
        
        """
        if not nodes:
            raise ValueError('Select any nodes')


        cmds.select(nodes)
        if (startframe is None) or (endframe is None):
            cmds.mayaUSDExport(file=filepath, selection=True, exportInstances=True)

        else:
            cmds.mayaUSDExport(
                file=filepath,
                selection=True,
                exportInstances=True,
                frameRange=[int(startframe), int(endframe)],
                frameStride=1.0,
            )


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
    

    def get_camera_shape(self, node: str) -> str:
        """ カメラのシェイプノードを取得 """
        if cmds.objectType(node, isType='camera'):
            return node

        elif cmds.objectType(node, isType='transform'):
            camera_shape = cmds.listRelatives(node, shapes=True, type='camera')[0]

            if camera_shape:
                return camera_shape
            else:
                return None


    def get_camera_shape_from_selection(self) -> str:
        """ 選択しているカメラのシェイプノードを取得 """
        _nodes = cmds.ls(sl=True)

        if _nodes:
            return self.get_camera_shape(_nodes[0])

        

    def get_current_render(self) -> str:
        return cmds.getAttr('defaultRenderGlobals.currentRenderer')

    def get_ext(self, key: str = None) -> str:
        """ 拡張子を返す 
        
        """
        if key is None:
            return '.ma'
        
        else:
            return EXT_DICT.get(key.lower())
            

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    
    
    def get_filename(self) -> str:
        """現在開いているファイル名を取得"""
        _filepath = self.get_filepath()

        if _filepath:
            return pathlib.Path(_filepath).name

    

    def get_filepath(self) -> str:
        return cmds.file(q=True, sceneName=True)
    

    def get_fps(self) -> int:
        fps_dict = {
            "game": 15,
            "film": 24,
            "pal": 25,
            "ntsc": 30,
            "show": 48,
            "palf": 50,
            "ntscf": 60
        }

        fps = cmds.currentUnit(query=True, time=True)
        return fps_dict.get(fps)


    

    def get_framerange(self) -> tuple[int]:
        headin = cmds.playbackOptions(q=True, ast=True)
        tailout = cmds.playbackOptions(q=True, aet=True)
        cutin = cmds.playbackOptions(q=True, min=True)
        cutout = cmds.playbackOptions(q=True, max=True)

        return headin, cutin, cutout, tailout
    

    def get_imageplane(self, camera, create=True) -> str:
        _imageplane = cmds.listConnections(f'{camera}.imagePlane', type='imagePlane')
        _plane = None

        if _imageplane:
            _plane = _imageplane[0]

        else:
            if create:
                _imageplane = cmds.imagePlane(camera=camera)
                _plane = _imageplane[1]
            
        return _plane

    def get_main_window(self):
        """ Mayaのメインウィンドウを取得 
        
        """
        ptr = omui.MQtUtil.mainWindow()

        if ptr is not None:
            return wrapInstance(int(ptr), QtWidgets.QWidget)
        

    def get_render(self) -> str:
        return cmds.getAttr('defaultRenderGlobals.currentRenderer')

        

    def get_render_size(self) -> tuple[int]:
        _render = self.get_render()

        if _render == 'vray':
            vray_setting = 'vraySettings'
            _width = cmds.getAttr(f'{vray_setting}.width')
            _height = cmds.getAttr(f'{vray_setting}.height')

            return _width, _height
        
        else:
            _width = cmds.getAttr('defaultResolution.width')
            _height = cmds.getAttr('defaultResolution.height')

            return _width, _height

        

    def get_selected_nodes(self) -> list[str]:
        """ 選択しているノードを返す
        
        Returns:
            list[str]: 選択しているノードリスト
        """
        return cmds.ls(sl=True)


    def import_file(self, filepath, namespace=None):    
        if os.path.exists(filepath):
            file, ext = os.path.splitext(filepath)

            if namespace is None:
                if self.is_usd(filepath):
                    # pm.importFile(filepath, type='USD Import',preserveReferences=True)
                    return cmds.file(filepath, i=True, type='USD Import', preserveReferences=True)
                
                elif self.is_image(filepath):
                    self.import_texture(filepath)

                elif self.is_maya(filepath):
                    # pm.importFile(filepath, preserveReferences=True)
                    return cmds.file(filepath, i=True)
                else:
                    raise TypeError('MDK | Not supported file type')
                
            else:
                currentNs = cmds.namespaceInfo(cur=True)

                if not cmds.namespace(ex=':{}'.format(namespace)):
                    cmds.namespace(add=':{}'.format(namespace))

                cmds.namespace(set=':{}'.format(namespace))

                return cmds.file(filepath, i=True, mergeNamespacesOnClash=False, namespace=namespace)
                        
        else:
            raise FileNotFoundError()
        

    def import_files(self, filepath_list: list[str], namespace=None):
        for _filepath in filepath_list:
            self.import_file(_filepath, namespace=namespace)


    def import_texture(self, filepath, colorspace=None):
        node_name = pathlib.Path(filepath).stem
        # file_node = cmds.shadingNode('file', asShader=True, name=node_name)
        file_node = cmds.shadingNode('file', asShader=True)

        cmds.setAttr(file_node + '.fileTextureName', filepath, type='string')

        # place2d_node = cmds.shadingNode('place2dTexture', asUtility=True, name=place2d_name)
        place2d_node = cmds.shadingNode('place2dTexture', asUtility=True)

        # Fileノードに2Dプレースメントノードを接続
        cmds.connectAttr(place2d_node + '.outUV', file_node + '.uvCoord')
        cmds.connectAttr(place2d_node + '.outUvFilterSize', file_node + '.uvFilterSize')

        if colorspace:
            cmds.setAttr(f'{file_node}.ignoreColorSpaceFileRules', 1)
            cmds.setAttr(f'{file_node}.colorSpace', colorspace, type='string')

        return file_node


        
    def is_abc(self, filepath: str) -> tuple:
        """ Alembicファイル判定 """
        return FILE_FILTER_ABC.match(filepath)
        
    def is_fbx(self, filepath: str) -> tuple:
        """ Alembicファイル判定 """
        return FILE_FILTER_FBX.match(filepath)
        
    def is_image(self, filepath: str) -> tuple:
        """ イメージファイル判定 """
        return FILE_FILTER_IMAGE.match(filepath)
       
    def is_maya(self, filepath: str) -> tuple:
        """ Mayaファイル判定 """
        return FILE_FILTER_MAYA.match(filepath)
       
    def is_obj(self, filepath: str) -> tuple:
        """ Objファイル判定 """
        return FILE_FILTER_OBJ.match(filepath)
    
    def is_usd(self, filepath: str) -> tuple:
        """ USDファイル判定 """
        return FILE_FILTER_USD.match(filepath)
    

    def open_dir(self):
        """
        フォルダを開く。
        ノードを選択していなければ、現在のファイルのフォルダ
        ノードを選択していれば、ノードタイプに基づいたフォルダを開く
        """
        _nodes = cmds.ls(sl=True)

        if len(_nodes)==0:
            _filepath = self.get_filepath()
            open_in_explorer(_filepath)


        else:
            for _node in _nodes:
                _filepath = None
                _node_type = cmds.nodeType(_node)

                if _node_type == 'file':
                    _filepath = cmds.getAttr(f'{_node}.fileTextureName')

                    if _filepath:
                        open_in_explorer(_filepath)



    def open_file(self, filepath, recent=False):
        """ Plugin Builtin Function """
        if recent:
            self.add_recent_file(filepath)

        cmds.file(filepath, open=True, force=True)
        

    def reference_file(self, filepath: str, namespace: str=None):
        """ ファイルをリファレンス

        Updated 2024/02/14 Yamagishi
            * namaspcae 判定に or namespace == '' を追加

        Args:
            plugin(object): パイプライン用Mayaプラグインクラス
            filepath(str): リファレンスするファイル
            namespace(:obj:`str`, optional): namespace=None
        """
        # cmds.createReference(filepath, ns=namespace)
        
        if (namespace is None) or (namespace ==''):
            namespace = ':'

        return cmds.file(filepath, reference=True, mergeNamespacesOnClash=True, namespace=namespace)


    def reference_files(self, filepath_list: list[str], namespace: str=None):
        """ 複数ファイルをリファレンス

        Args:
            filepaths(list[str]): リファレンスするファイルリスト
            namespace(:obj:`str`, optional): namespace=None
        """
        for _filepath in filepath_list:
            self.reference_file(_filepath, namespace=namespace)


    def select_nodes(self, nodes: list[str]):
        """ ノードを選択 
        
        Args:
            nodes(list[str]): 選択するノードリスト
        """
        cmds.select(nodes, r=True)


    def set_camera_image_plane(self, filepath: str):
        """ 選択しているカメラにカメライメージプレーンを設定 """
        _camera_shape = self.get_camera_shape_from_selection()
        _plane = self.get_imageplane(_camera_shape, create=True)

        cmds.setAttr(f'{_plane}.imageName', filepath, type='string')
        cmds.setAttr(f'{_plane}.useFrameExtension', 1)
        cmds.setAttr(f'{_plane}.ignoreColorSpaceFileRules', 1)
        cmds.setAttr(f'{_plane}.colorSpace', 'sRGB - Texture', type='string')


    def set_fps(self, value: int):
        fps_dict = {
            15: "game",
            24: "film",
            25: "pal",
            30: "ntsc",
            48: "show",
            50: "palf",
            60: "ntscf"
        }

        value = int(float(value)+0.5)

        cmds.currentUnit(time=fps_dict[value])


    def set_framerange(self, headin: int, cutin: int, cutout: int, tailout: int):
        cmds.playbackOptions(animationStartTime=headin, animationEndTime=tailout)
        cmds.playbackOptions(minTime=headin, maxTime=tailout)
        cmds.currentTime(headin)


    def set_render(self, renderer):
        render_globals_node = cmds.ls(type='renderGlobals')[0]
        cmds.setAttr(render_globals_node + '.currentRenderer', renderer, type='string')

        if renderer == 'vray':
            if not cmds.ls('vraySettings'):
                cmds.shadingNode("VRaySettingsNode", asUtility=True, name = "vraySettings")
        
        elif renderer == 'arnold':
            if not cmds.ls('defaultArnoldRenderOptions'):
                cmds.shadingNode("aiOptions", asUtility=True, name = "defaultArnoldRenderOptions")

        print(f'set render = {renderer}')

    def set_render_framerange(self, first_frame, last_frame):
        renderer = self.get_render()

        if renderer == 'arnold':
            node = 'defaultRenderGlobals'
            cmds.setAttr(f'{node}.outFormatControl', 0)
            cmds.setAttr(f'{node}.animation', 1)
            cmds.setAttr(f'{node}.putFrameBeforeExt', 1)
            cmds.setAttr(f'{node}.periodInExt', 1)
            cmds.setAttr(f'{node}.extensionPadding', 4)

            cmds.setAttr(f'{node}.startFrame', first_frame)
            cmds.setAttr(f'{node}.endFrame', last_frame)


        elif renderer =='vray':
            node = 'vraySettings'
            cmds.setAttr(f'{node}.animType', 1)
            cmds.setAttr(f'{node}.animBatchOnly', 1)

            cmds.setAttr(f'defaultRenderGlobals.startFrame', first_frame)
            cmds.setAttr(f'defaultRenderGlobals.endFrame', last_frame)

    def set_render_size(self, width, height):
        print(f'set render size = {width} x {height}')

        cmds.setAttr("defaultResolution.aspectLock", 0)
        renderer = self.get_render()

        if renderer == 'vray':
            vray_setting = 'vraySettings'
            cmds.setAttr(f'{vray_setting}.aspectLock', 0)
            cmds.setAttr(f'{vray_setting}.width', width)
            cmds.setAttr(f'{vray_setting}.height', height)
            cmds.setAttr(f'{vray_setting}.pixelAspect', 1.0)
            cmds.setAttr(f'{vray_setting}.aspectLock', True)

        else:
            default_resolution = 'defaultResolution'
            cmds.setAttr(f'{default_resolution}.width', int(width))
            cmds.setAttr(f'{default_resolution}.height', int(height))




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
            '.obj': 'OBJexport',
        }

        _nodes = cmds.ls(sl=True)
        if not _nodes:
            RuntimeError('Select any node')

        _, _ext = os.path.splitext(filepath)
        _ext = _ext.lower()
        _filetype = filetype_dict.get(_ext)

        cmds.file(filepath, force=True, type =_filetype, exportSelected=True)


    def start_end_infinity(self, node, start_frame, end_frame):
        """ 
        nodeのスタートとエンドInfityを設定
        """
        # animation key edit
        for attr in ATTR_LIST:
            cam_connection = cmds.connectionInfo(node + '.' + attr, sourceFromDestination=True)
            if cam_connection:
                object_type = cmds.objectType(cam_connection)
                if object_type == 'animCurveTA' or 'animCurveTL':
                    cmds.selectKey(clear=True)
                    anim_key = cam_connection.split('.', 1)[0]
                    cmds.selectKey(anim_key, add=True, time=(start_frame, start_frame), keyframe=True)
                    cmds.selectKey(anim_key, add=True, time=(end_frame, end_frame), keyframe=True)
                    cmds.keyTangent(e=True, itt='spline', ott='spline')  # start/end tangent type spline
                    cmds.setInfinity(pri='linear', poi='linear')  # start/end infinity setting

        mel.eval("animCurveEditor -edit -displayInfinities true graphEditor1GraphEd; optionVar -intValue graphEditorDisplayInfinities true;")
    

    def warning_dialog(self, message: str):
        """ 警告ダイアログ """
        cmds.confirmDialog(
				title = 'Warning',
				message = message,
				button=['Yes'],
                defaultButton='Yes',)