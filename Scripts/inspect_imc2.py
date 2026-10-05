import unreal as u, pathlib, json
paths=['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/Input/IMC_Default']
out={}
for p in paths:
    a=u.load_asset(p); d={'class':a.get_class().get_name() if a else None}
    if a:
        for prop in ['mappings','default_key_mappings']:
            try:
                arr=a.get_editor_property(prop); d[prop]=[]
                # default_key_mappings may contain key_mappings
                if hasattr(arr,'get_editor_property'):
                    try: arr=arr.get_editor_property('key_mappings')
                    except Exception: pass
                for m in arr:
                    item={}
                    for x in ['action','key']:
                        try: item[x]=str(m.get_editor_property(x))
                        except Exception as e: item[x]='ERR '+str(e)
                    d[prop].append(item)
            except Exception as e: d[prop]='ERR '+str(e)
    out[p]=d
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/imc_report2.json'); path.write_text(json.dumps(out,indent=2)); print(path)
