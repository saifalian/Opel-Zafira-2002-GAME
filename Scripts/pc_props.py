import unreal as u,json,pathlib,traceback
r={}
try:
 b=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
 cls=u.EditorAssetLibrary.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
 cdo=u.get_default_object(cls)
 r['class']=str(cls)
 for p in ['touch_controls_widget_class','TouchControlsWidgetClass','vehicle_hud_class','VehicleHudClass']:
  try: r[p]=str(cdo.get_editor_property(p))
  except Exception as e: r[p]='ERR '+str(e).split('\n')[0]
except Exception: r['err']=traceback.format_exc()
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/pc_props.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))