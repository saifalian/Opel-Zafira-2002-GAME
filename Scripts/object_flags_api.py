import unreal as u, pathlib, json
out={}
try:
    out['ObjectFlags']=[x for x in dir(u.ObjectFlags) if x.isupper() or x.startswith('RF')]
    out['Object_methods']=[x for x in dir(u.Object) if 'flag' in x.lower() or 'outer' in x.lower() or 'package' in x.lower()]
except Exception as e: out['error']=str(e)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/object_flags_api.json'); path.write_text(json.dumps(out,indent=2)); print(path)
