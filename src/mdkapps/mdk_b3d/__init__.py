""" mdk_b3d
 
* VFX用Blender互換パッケージ

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2024-11-15 Tatsuya Yamagishi
        * added: path
"""

VERSION = 'v0.0.1'
NAME = 'mdk_b3d'

import os
import re
import sys

import bpy

if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdk_b3d package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')



#=======================================#
# Settings
#=======================================#
FILE_FILTER_USD = re.compile(r'.+\.(usd|usdc|usda)')

EXT_LIST = [
    '.b3d',
    '.abc',
    '.fbx',
    '.obj',
    '.usd',
]


EXT_DICT = {
    'asset': '.b3d',
    'geo': '.abc',
    'shot': '.b3d',
    'usd': '.usd',
}
#=======================================#
# Functions
#=======================================#
def context_window(func):
    """
    Reference from : https://blender.stackexchange.com/questions/269960/bpy-context-object-changes-within-pyside2-button-callback
    
    Support running operators from QT (ex. on button click).
    Decorator to override the context window for a function,
    """
    def wrapper(*args, **kwargs):
        with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
            return func(*args, **kwargs)

    return wrapper



def create_playblast(filepath: str, size: list|tuple=None, range: list|tuple=None, filetype='jpg'):
    """ プレイブラストを作成
    
    Args:
        filepath(str): 出力ファイルパス
        size(list | turple): サイズ
        range(list | turple): サイズ
    """

    raise RuntimeError('未実装')

#=======================================#
# Class
#=======================================#
class AppMain:
    def __init__(self):
        pass

    def get_ext(self, key: str = None) -> str:
        return '.b3d'

    def get_ext_list(self):
        """ 拡張子リストを返す"""
        return list(EXT_LIST)
    

    def get_framerange(self):
        """ フレームレンジを取得
        """
        _start_frame = bpy.context.scene.frame_start
        _end_frame = bpy.context.scene.frame_end
        return _start_frame, _start_frame, _end_frame, _end_frame
    
    @context_window
    def import_abc(self, filepath: str):
        """
        
        """
        bpy.ops.wm.alembic_import(filepath=filepath)

    def import_file(self, filepath: str):
        """ ファイルをインポート
        """
        if self.is_usd(filepath):
            self.import_usd(filepath)
        elif self.is_abc(filepath):
            self.import_abc(filepath)

    def import_files(self, filepath_list: list[str], namespace=None):
        for _filepath in filepath_list:
            self.import_file(_filepath, namespace=namespace)


    @context_window
    def import_usd(self, filepath: str, scale: float = 0.01):
        """ USDファイルをインポート

        Reference from:

        * https://devtalk.blender.org/t/issue-with-importing-usd-files-via-bpy-ops-wm-usd-import-and-python/26152

        bpy.ops.wm.usd_import(
            filepath=self.file_path, 
            import_cameras=True, 
            import_curves=True, 
            import_lights=True, 
            import_materials=True, 
            import_meshes=True, 
            import_volumes=True, 
            scale=1.0, 
            read_mesh_uvs=True, 
            read_mesh_colors=False, 
            import_subdiv=False, 
            import_instance_proxies=True, 
            import_visible_only=True,
            import_guide=False,
            import_proxy=True,
            import_render=True,
            set_frame_range=True,
            relative_path=True,
            create_collection=False,
            light_intensity_scale=1.0,
            mtl_name_collision_mode='MAKE_UNIQUE',
            import_usd_preview=True,
            set_material_blend=True)
        """
        # _override = get_override_context()

        bpy.ops.wm.usd_import(
                # _override,
                filepath=filepath,
                scale=scale,)


    def is_usd(self, filepath: str) -> tuple:
        """ USDファイル判定 """
        return FILE_FILTER_USD.match(filepath)
    

    @context_window
    def save_file(self, filepath, context=False):
        if context:
            _override = bpy.context.copy()
            _override['blend_data'] = bpy.data

            bpy.ops.wm.save_as_mainfile(_override, filepath=filepath)

        else:
            bpy.ops.wm.save_as_mainfile(filepath=filepath)