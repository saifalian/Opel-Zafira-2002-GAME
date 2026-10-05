import unreal as u, pathlib, json
classes=[u.BlueprintEditorLibrary]
try: classes.append(u.BlueprintGraphLibrary)
except Exception: pass
try: classes.append(u.BlueprintGraphEditor)
except Exception: pass
out={c.__name__:[n for n in dir(c) if 'node' in n.lower() or 'graph' in n.lower() or 'blueprint' in n.lower()] for c in classes}
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/bp_api2.json'); path.write_text(json.dumps(out,indent=2)); print(path)
