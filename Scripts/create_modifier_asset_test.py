import unreal as u, pathlib, json, traceback
out={}
try:
    at=u.AssetToolsHelpers.get_asset_tools()
    asset=at.create_asset('ZafiraInputNegate_Test','/Game/VehicleTemplate/Input',u.InputModifierNegate,None)
    out['asset']=str(asset)
    if asset: u.EditorAssetLibrary.save_loaded_asset(asset,False)
except Exception: out['error']=traceback.format_exc()
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/create_modifier_asset_report.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
