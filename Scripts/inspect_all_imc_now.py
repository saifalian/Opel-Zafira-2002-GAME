import unreal as u, pathlib, json
out={}
for p in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/VehicleTemplate/Input/IMC_SteeringWheel','/Game/VehicleTemplate/Input/IMC_Vehicle_MouseLook','/Game/Input/IMC_Default']:
    a=u.load_asset(p)
    if a:
        try: out[p]=[m.export_text() for m in a.get_editor_property('default_key_mappings').get_editor_property('mappings')]
        except Exception as e: out[p]='ERR '+str(e)
    else: out[p]='missing'
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/all_imc_now.json'); path.write_text(json.dumps(out,indent=2)); print(path)
