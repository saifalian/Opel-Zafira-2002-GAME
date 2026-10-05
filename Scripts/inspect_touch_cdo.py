import unreal as u, json, pathlib, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
try:
    for path in ['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController','/Game/VehicleTemplate/Input/UI_Touch_Vehicle','/Game/Input/Touch/UI_TouchSimple']:
        obj=u.load_asset(path)
        d={'asset_class':str(obj.get_class().get_name()) if obj else None,'cdo_props':{},'cdo_class':None}
        if obj:
            gen=None
            for attr in ['generated_class','GeneratedClass']:
                try:
                    v=getattr(obj,attr)
                    gen=v() if callable(v) else v
                    if gen: break
                except Exception: pass
            d['gen']=str(gen)
            if gen:
                try:
                    cdo=u.get_default_object(gen); d['cdo_class']=str(cdo.get_class().get_name())
                    names=[]
                    try: names=list(cdo.get_editor_property_names())
                    except Exception: names=[n for n in dir(cdo)]
                    for n in names:
                        sn=str(n)
                        if any(s in sn.lower() for s in ['touch','widget','button','mobile','input','steer','left','right','control']):
                            try: d['cdo_props'][sn]=str(cdo.get_editor_property(sn))
                            except Exception as e: d['cdo_props'][sn]='ERR '+str(e)
                except Exception as e: d['cdo_error']=str(e)
        report[path]=d
except Exception:
    report={'error':traceback.format_exc()}
(P/'Scripts/touch_cdo_inspect.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))