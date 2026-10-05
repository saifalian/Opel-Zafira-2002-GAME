import unreal as u,json,pathlib
r={'unreal_funcs':[x for x in dir(u) if 'object' in x.lower() or 'asset' in x.lower()][:200]}
# Try known UI object names guessed from buttons
prefix='/Game/VehicleTemplate/Input/UI_Touch_Vehicle.UI_Touch_Vehicle:WidgetTree.'
for n in ['CanvasPanel','CanvasPanel_0','LeftThumbstick','RightThumbstick','Throttle','Brake','Handbrake','Reset','Image','TextBlock']:
    o=u.find_object(None,prefix+n); r[n]=str(o)
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/obj_api.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))