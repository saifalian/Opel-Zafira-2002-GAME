import unreal as u,json,pathlib
cls=u.EditorAssetLibrary.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
cdo=u.get_default_object(cls)
r={}
for name in dir(cdo):
 if any(s in name.lower() for s in ['touch','hud','widget','class']):
  try: r[name]=str(getattr(cdo,name))
  except Exception as e: r[name]='ERR'
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/pc_dir.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))