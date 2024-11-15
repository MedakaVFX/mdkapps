""" mdkapps インポートテスト
 
* モジュールの読み込み用テストコード

Info:
    * Created : v0.0.1 2024-11-15 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>
 
Release Note:
    * v0.0.1 2024-11-15 Tatsuya Yamagishi
        * New
"""
import logging
import os
import sys

os.environ['MDK_DEBUG']='1'
sys.path.append(os.path.dirname(__file__)+'/../src')

import mdkapps



def get_logger():
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False

    _stream_handler = logging.StreamHandler()
    _stream_handler.setFormatter(logging.Formatter(
        '[%(levelname)s][%(name)s][%(funcName)s:%(lineno)s] %(message)s'))
    _logger.addHandler(_stream_handler)

    return _logger



if __name__ == '__main__':
    logger = get_logger()

    _filepath = r'C:\Users\ta_yamagishi\temp\test.png'
    _size = [1920, 1080]
    _range = [1001, 1200]

    logger.info(f'MDK | -------------------------------')
    logger.info(f'MDK | [Create Playblast]')
    logger.info(f'MDK | {_filepath}')
    logger.info(f'MDK | {_size}')
    logger.info(f'MDK | {_range}')

    mdkapps.create_playblast(_filepath, _size, _range)