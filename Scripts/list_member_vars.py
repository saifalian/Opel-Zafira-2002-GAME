import unreal as u, pathlib, json, traceback
out={}
for p in ['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase','/Game/Zafira/BP_Zafira']:
    try:
        bp=u.load_asset(p); names=u.BlueprintEditorLibrary.list_member_variable_names(bp); out[p]=[str(n) for n in names]
    except Exception as e: out[p]='ERR '+str(e)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/member_vars.json'); path.write_text(json.dumps(out,indent=2)); print(path)
