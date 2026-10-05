import unreal as u, pathlib, json
w=u.ChaosWheelSetup()
out={}
for p in ['wheel_class','bone_name','additional_offset']:
    try: out[p]=str(w.get_editor_property(p))
    except Exception as e: out[p]='ERR '+str(e)
out['export']=w.export_text()
out['tuple']=str(w.to_tuple())
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/wheel_setup_api.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
