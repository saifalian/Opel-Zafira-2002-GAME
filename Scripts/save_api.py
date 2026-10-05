import unreal as u, pathlib, json
mods=[u.EditorLoadingAndSavingUtils,u.EditorLevelLibrary]
out={m.__name__ if hasattr(m,'__name__') else str(m): [x for x in dir(m) if 'save' in x.lower() or 'map' in x.lower()] for m in mods}
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/save_api.json'); path.write_text(json.dumps(out,indent=2)); print(path)
