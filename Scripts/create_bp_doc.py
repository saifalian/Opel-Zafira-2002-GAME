import unreal as u, pathlib
out=str(u.BlueprintEditorLibrary.create_blueprint_asset_with_parent.__doc__)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/create_bp_doc.txt'); path.write_text(out); print(path)
