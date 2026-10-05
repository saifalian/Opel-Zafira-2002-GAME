import unreal as u, pathlib, json
m=u.new_object(u.InputModifierNegate)
out={'dir':[x for x in dir(m) if 'flag' in x.lower() or 'outer' in x.lower() or 'package' in x.lower() or 'root' in x.lower()]}
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/modifier_methods.json'); path.write_text(json.dumps(out,indent=2)); print(path)
