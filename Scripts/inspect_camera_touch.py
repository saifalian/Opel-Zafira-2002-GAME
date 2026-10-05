import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
try:
    paths=['/Game/VehicleTemplate/Input/IMC_Vehicle_MouseLook','/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/VehicleTemplate/Input/TI_ZafiraMobile','/Game/VehicleTemplate/Input/TI_ZafiraRequestedMobile']
    for p in paths:
        o=u.load_asset(p); d={'class':str(o.get_class().get_name()) if o else None}
        if o:
            try: d['export']=o.export_text()
            except Exception as e: d['export_error']=str(e)
            for prop in ['controls','mappings','default_key_mappings']:
                try: d[prop]=str(o.get_editor_property(prop))
                except Exception as e: pass
        report[p]=d
except Exception:
    report={'error':traceback.format_exc()}
(P/'Scripts/inspect_camera_touch.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))