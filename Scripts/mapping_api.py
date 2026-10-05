import unreal as u, pathlib, json
ia=u.load_asset('/Game/VehicleTemplate/Input/Actions/IA_Steering')
imc=u.load_asset('/Game/VehicleTemplate/Input/IMC_Vehicle_Default')
k=u.Key(); k.set_editor_property('key_name','A')
m=imc.map_key(ia,k)
out={'mapping_class':m.__class__.__name__,'props':[p for p in dir(m) if not p.startswith('_')][:200]}
for p in ['action','key','modifiers','triggers','player_mappable_options']:
    try: out[p]=str(m.get_editor_property(p))
    except Exception as e: out[p]='ERR '+str(e)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/mapping_api.json'); path.write_text(json.dumps(out,indent=2)); print(path)
imc.unmap_all()
