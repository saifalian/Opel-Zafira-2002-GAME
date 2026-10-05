import unreal as u, pathlib, json
out={}
classes=[u.InputMappingContext]
for c in classes: out[c.__name__]=[n for n in dir(c) if 'map' in n.lower() or 'key' in n.lower() or 'mapping' in n.lower()]
# doc
for n in out['InputMappingContext']:
    try: out['doc_'+n]=str(getattr(u.InputMappingContext,n).__doc__)
    except Exception: pass
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/enhanced_api.json'); path.write_text(json.dumps(out,indent=2)); print(path)
