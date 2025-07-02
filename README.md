# mdkapplibs
App互換Pythonライブラリ

対応Appリスト
| App | Description |
| --- | --- |
| Blender | |
| Cinema4D | |
| Houdini | |
| Max | |
| Maya | |
| Nuke | |
| Standalone | |


## v0.0.1 2025/05/22
- added : New

## Examples
```python
import mdkapps

_filepath = r'C:\Users\ta_yamagishi\temp\test'
_size = [1920, 1080]
_range = [1001, 1200]

mdkapps.create_playblast(_filepath, _size, _range, filetype='png')
```

Using in Maya
<img width="400" src="https://i.gyazo.com/395cadc7f2596a3bb8e4d7a36861b3e2.png">


## Commands
| Functions | Args | Description |
| --- | --- | --- |
| create_playblast | filepath: str<br>size: list or tuple<br>range: list or tuple | プレイブラストを作成 |