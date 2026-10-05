import unreal as u, pathlib, json
names=[n for n in dir(u) if 'InputModifier' in n or 'InputTrigger' in n]
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/input_classes.json'); path.write_text(json.dumps(names,indent=2)); print(path)
