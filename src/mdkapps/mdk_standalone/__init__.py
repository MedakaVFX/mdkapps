""" mdk_standalone
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya Yamagishi
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2025-01-31 Tatsuya Yamagishi
        * New
"""

VERSION = 'v0.0.1'
NAME = 'mdk_standalone'

import os
import pathlib
import platform
import re
import subprocess
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
    '.abc',
    '.fbx',
    '.usd',
]

EXT_DICT = {
    'asset': '.dat',
    'shot': '.txt',
    'geo': '.abc',
    'usd': '.usd',
}

FILE_FILTER_SCRIPT = re.compile(r'.+\.(py)')
# ======================================= #
# Functions
# ======================================= #
# ======================================= #
# Class
# ======================================= #
class AppMain:
    def __init__(self):
        self.FILE_FILTER_SCRIPT = FILE_FILTER_SCRIPT

    # --------------------------------- #
    # Get / Set
    # --------------------------------- #
    def get_ext(self, key: str = None) -> str:
        """ 拡張子を返す 
        
        """
        if key is None:
            return '.dat'
        
        if type(key) is not str:
            raise TypeError('key is not str.')


        return EXT_DICT.get(key.lower())
    

    def get_default_ext(self) -> str:
        """ デフォルト拡張子を返す """
        return '.txt'

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    

    def get_filename(self) -> str:
        """現在開いているファイル名を取得"""
        _filepath = self.get_filepath()

        if _filepath:
            return pathlib.Path(_filepath).name

    
    def get_filepath(self) -> str:
        """現在開いているファイルパスを取得"""
        return None
    
    def get_fps(self) -> float:
        return 24.000
    
    def get_framerange(self) -> tuple[int]:
        """フレームレンジを取得"""
        return (1001, 1001, 1200, 1200)

    def get_render_size(self) -> tuple[int]:
        """ レンダーサイズを取得 """
        return (1920, 1080)

    def get_selected_nodes(self) -> list[str]:
        """ 選択しているノードを取得 """
        return ['root', 'root/geo']
    
    def set_aperture_size(self, values: tuple[int]):
        print(f'MDK | aperture_size = {values}')

    def set_fps(self, value: str):
        print(f'MDK | fps = {value}')

    def set_framerange(self, values: tuple[int]):
        print(f'MDK | framerange = {values}')

    def set_render_size(self, values: tuple[int]):
        print(f'MDK | render_size = {values}')

    def set_render(self, value: str):
        print(f'MDK | render = {value}')

    def set_render_framerange(self, first: int, last: int):
        print(f'MDK | render_framerange = {first} - {last}')

    def set_unit(self, value: str):
        print(f'MDK | unit = {value}')

    # --------------------------------- #
    # Methods
    # --------------------------------- #
    def create_playblast(self,
                    filepath: str,
                    size: list|tuple=None,
                    range: list|tuple=None,
                    ext: str = '.jpg',
                    mp4: bool = False):
        
        print('# --------------------------------- #')
        print('# Create Playblast')
        print('# --------------------------------- #')

        print(f'Size: {size}')
        print(f'Ext: {ext}')
        print(f'Range: {range}')
        print(f'Mp4: {mp4}')
        print(f'Filepath: {filepath}')


    def select_nodes(self, nodes: list[str]):
        """ ノードを選択 """
        print(f'MDK | select = {nodes}')
    
    
    def warning_dialog(self, message: str):
        """ 警告ダイアログ """
        print(f'MDK | warning = {message}')

        
    # --------------------------------- #
    # I/O
    # --------------------------------- #
    def import_file(self, filepath: str):
        print(f'MDK | Standard | import = {filepath}')


    def import_files(self, filepath_list: list[str]):
        for _filepath in filepath_list:
            self.import_file(_filepath)

    def import_usd(self, filepath: str):
        print(f'MDK | USD | import = {filepath}')


    def open_file(self, filepath: str):
        print(f'MDK | open = {filepath}')

        if os.path.isfile(filepath):
            if platform.system() == 'Windows':
                cmd = 'explorer {}'.format(filepath.replace('/', '\\'))
                subprocess.Popen(cmd)
            
            elif platform.system() == 'Darwin':
                subprocess.call(['open', filepath])
            
            else:
                subprocess.Popen(["xdg-open", filepath])
        else:
            raise TypeError('"filepath" is not file.')
        
        


    def reference_file(self, filepath: str, namespace=None):
        print(f'MDK | reference = {filepath}')


    def reference_files(self, filepath_list: list[str], namespace=None):
        for _filepath in filepath_list:
            self.reference_file(_filepath, namespace=namespace)


    def save(self):
        """ 上書き保存 """
        pass
    
    
    def save_file(self, filepath):
        _filepath = pathlib.Path(filepath)
        # _file.parent.mkdir(parents=True, exist_ok=True)
        _filepath.write_text('Medaka', encoding='utf8')


    def save_selection(self, filepath: str):
        """ 選択を保存 """
        _nodes = self.get_selected_nodes()

        _filepath = pathlib.Path(filepath)
        _filepath.write_text(str(_nodes), encoding='utf8')
