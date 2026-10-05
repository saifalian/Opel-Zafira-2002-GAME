import unreal as u, pathlib, json
imc=u.load_asset('/Game/VehicleTemplate/Input/IMC_Vehicle_Default')
d=imc.get_editor_property('default_key_mappings')
out={'class':d.__class__.__name__,'dir':[x for x in dir(d) if not x.startswith('_')], 'tuple':None,'dict':None}
try: out['tuple']=str(d.to_tuple())
except Exception as e: out['tuple']='ERR '+str(e)
try: out['dict']=d.to_dict()
except Exception as e: out['dict']='ERR '+str(e)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/default_key_mappings_struct.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
