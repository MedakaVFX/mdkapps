""" mdk_max
 
* VFX用3dsMax互換パッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.2 (v0.0.2) 2025-03-31 Tatsuya Yamagishi
        * added: FILE_FILTER_SCRIPT
        * added: create_playblast

    * v0.0.1 (v0.0.1) 2024-11-15 Tatsuya Yamagishi
        * added: path
"""

VERSION = 'v0.0.2'
NAME = 'mdk_max'

import os
import platform
import re
import subprocess
import sys

import pymxs
rt = pymxs.runtime

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except:
    from qtpy import QtCore, QtGui, QtWidgets


if os.environ.get('MDK_DEBUG'):
    print('MdkMax | ---------------------------')
    print('MdkMax | [ import mdk_max package]')
    print(f'MdkMax | {NAME} {VERSION}')
    print('MdkMax | ---------------------------')

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


FILE_FILTER_SCRIPT = re.compile(r'.+\.(py|ms)')

#=======================================#
# Functions
#=======================================#
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
        self.FILE_FILTER_SCRIPT = FILE_FILTER_SCRIPT

    def create_playblast(
                    self,
                    filepath: str,
                    size: list|tuple=None,
                    framerange: list|tuple=None,
                    filetype='png'
                    ):

        """ プレイブラストを作成
        
        Args:
            filepath(str): 出力ファイルパス
            size(list | turple): サイズ
            range(list | turple): サイズ
        """

        # for frame in range(framerange[0], framerange[1] + 1):
        #     rt.sliderTime = frame  # フレームを移動
        #     image_path = f'{filepath}.{frame:04d}.{filetype}'
        #     rt.maxOps.CaptureViewport(image_path, size[0], size[1], True)

        _fps = self.get_fps()

        cmd = f"""
            max preview 
            outputAVI:false
            outputImageSeq:true
            filename:"{filepath}" 
            imageFormat: #png
            start: {framerange[0]}
            end: {framerange[1]}
            width: {size[0]}
            height: {size[1]}
            fps: {_fps}
        """
        rt.execute(cmd)
        
            
    def get_default_ext(self) -> str:
        """ デフォルト拡張子を返す """
        return '.max'


    def get_ext(self) -> str:
        """ 拡張子を返す 
        
        """
        return '.max'
    

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    

    def get_filepath(self) -> str:
        """現在開いているファイルパスを取得"""
        return f'{rt.maxFilePath}/{rt.maxFileName}'
    

    def get_fps(self) -> int:
        return rt.frameRate
    

    def get_framerange(self) -> tuple[int]:
        _start_frame = int(rt.animationRange.start.frame)
        _end_frame = int(rt.animationRange.end.frame)

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
    
    
    def get_render_size(self) -> tuple[int]:
        """ レンダーサイズを取得 """
        return (rt.renderWidth, rt.renderHeight)
    

    def import_file(self, filepath: str, namespace=None):
        """ ファイルをインポート
        """
        rt.importFile(filepath)


    def import_files(self, filepath_list: list[str], namespace=None):
        for _filepath in filepath_list:
            self.import_file(_filepath, namespace=namespace)


    def import_usd(self, filepath: str):
        print(f'MDKMax | import = {filepath}')

        rt.ImportFile(filepath, rt.Name("noPrompt"))


    def open_dir(self):
        print('MdkMax | Open Dir')

        _filepath = self.get_filepath()
        if os.path.exists(_filepath):
            open_in_explorer(_filepath)


    def open_file(self, filepath: str):
        rt.loadMaxFile(filepath, useFileUnits=True)


    def save_file(self, filepath: str):
        print(f'MdkMax | save = {filepath}')

        rt.saveMaxFile(filepath)


    def set_aperture_size(self, width: float, height: float):
        print(f'MdkMax | aperture_size = {width} x {height}')

        rt.setRendApertureWidth(float(width))

    def set_fps(self, value: int):
        print(f'MdkMax | fps = {value}')
        rt.frameRate = int(value+0.5)


    def set_framerange(self, headin: int, cutin: int, cutout: int, tailout: int):
        print(f'MdkMax | framerange = {headin} - {cutin} - {cutout} - {tailout}')

        rt.animationRange = rt.interval(headin, tailout)


    def set_render_size(self, height: int, width: int):
        print(f'MdkMax | render_size = {height} x {width}')
        
        rt.renderWidth = height
        rt.renderHeight = width


    def set_render(self, value: str):
        print(f'MdkMax | render = {value}')

        if value.lower() == 'arnold':
            rt.renderers.current = rt.Arnold()
        elif value.lower() == 'default':
            rt.renderers.current = rt.Default_Scanline_Renderer()
        elif value.lower() == 'vray':
            rt.renderers.current = rt.V_Ray_Adv_3_60_04()
        elif value.lower() == 'redshift':
            rt.renderers.current = rt.Redshift_Renderer()
        

    def set_render_framerange(self, first: int, last: int):
        print(f'MdkMax | render_framerange = {first} - {last}')
        rt.rendTimeType = 2

        rt.rendStart = first   # 開始フレーム
        rt.rendEnd = last      # 終了フレーム


    def set_unit(self, value: str):
        print(f'MdkMax | unit = {value}')

        if value.lower() == 'centimeter':
            rt.units.SystemType = rt.Name('Centimeters')