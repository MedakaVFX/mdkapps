""" mdklibs
 
* VFX用Pythonパッケージ

Info:
    * Created : v0.0.1 2024-11-01 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2024-11-01 Tatsuya Yamagishi
        * added: path
"""

VERSION = 'v0.0.1'
NAME = 'mdkapps'

import os
import sys


if os.environ.get('MDK_DEBUG'):
    print('MDK | ---------------------------')
    print('MDK | [ import mdkapps package]')
    print(f'MDK | {NAME} {VERSION}')
    print('MDK | ---------------------------')



try:
   """ Import Blender """
   import bpy
   print('MDK | Successfully imported Blender Python API bpy')
   from mdk_maya import *


except ImportError:
    try:
        """ Improt Cinema4D """
        import c4d
        from mdk_c4d import *

        print('MDK | Successfully imported Cinema4D Python API c4d')

    except ImportError:
        try:
            """ Improt Houdini """
            import hou
            from .mdk_houdini import *
            print('MDK | Successfully imported Hoduini Python API hou')

        except ImportError:
            try:
                """ Improt Max """
                import pymxs
                from .mdk_max import *
                print('MDK | Successfully imported 3dsMax Python API pymxs')

            except ImportError:
                try:
                    """ Improt Maya """
                    import maya.cmds as cmds
                    from .mdk_maya import *
                    print('MDK | Successfully imported Maya Python API maya.cmds')

                except ImportError:
                    try:
                        """ Improt nuke """
                        import nuke
                        from .mdk_nuke import *
                        print('MDK | Successfully imported Nuke Python API nuke')

                    except ImportError:
                        try:
                            """ Improt standalone """
                            from .mdk_standalone import *
                            print('MDK | Successfully imported Python API standalone')
                        except ImportError:
                            print("Failed to import all libraries. Please check your environment.")