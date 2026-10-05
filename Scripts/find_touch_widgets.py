import unreal as u,json,pathlib,traceback
r={}
try:
 b=u.load_asset('/Game/VehicleTemplate/Input/UI_Touch_Vehicle')
 wt=u.find_object(None,'/Game/VehicleTemplate/Input/UI_Touch_Vehicle.UI_Touch_Vehicle:WidgetTree')
 r['wt']=str(wt)
 for name in ['CanvasPanel_0','CanvasPanel','Thumbstick_Left','Gas','Brake','Button_Throttle','Button_Brake']:
  o=u.find_object(None,'/Game/VehicleTemplate/Input/UI_Touch_Vehicle.UI_Touch_Vehicle:WidgetTree.'+name); r[name]=str(o)
 # try all loaded objects names? no
except Exception: r['err']=traceback.format_exc()
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/find_touch_widgets.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))