import unreal as u, json, pathlib, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
try:
    for path in ['/Game/VehicleTemplate/Input/UI_Touch_Vehicle','/Game/Input/Touch/UI_TouchSimple','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController']:
        obj=u.load_asset(path)
        data={'class':str(obj.get_class().get_name()) if obj else None,'props':{},'dir':[]}
        if obj:
            names=[n for n in dir(obj) if any(s in n.lower() for s in ['widget','touch','button','input','left','right','steer','move','control'])]
            data['dir']=names[:200]
            try: props=obj.get_editor_property_names()
            except Exception: props=[]
            for n in props:
                if any(s in str(n).lower() for s in ['widget','touch','button','input','left','right','steer','move','control']):
                    try:data['props'][str(n)]=str(obj.get_editor_property(n))
                    except Exception as e:data['props'][str(n)]='ERR '+str(e)
            if hasattr(obj,'generated_class'):
                data['generated_class']=str(obj.generated_class)
        report[path]=data
except Exception:
    report={'error':traceback.format_exc()}
(P/'Scripts/touch_ui_inspect.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))