import unreal as u, pathlib, json
out={}
for p in ['/Game/Zafira/BP_WheelsFront','/Game/Zafira/BP_WheelsRear']:
    cls=u.EditorAssetLibrary.load_blueprint_class(p)
    cdo=u.get_default_object(cls)
    data={}
    for name in dir(cdo):
        if any(s in name.lower() for s in ['steer','engine','brake','radius','width','torque','hand','friction','wheel']):
            try: data[name]=str(cdo.get_editor_property(name))
            except Exception: pass
    out[p]=data
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/wheel_class_props.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
