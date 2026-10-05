import unreal,traceback,pathlib,json
try:exec(compile(pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/test_transmission.py').read_text(),'test_transmission.py','exec'))
except:
 pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/transmission_runtime_report.json').write_text(json.dumps({'error':traceback.format_exc()}));unreal.SystemLibrary.quit_editor()
