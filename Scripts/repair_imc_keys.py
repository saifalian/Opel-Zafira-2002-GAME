import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
r={}
def key(name):
    k=u.Key(); k.set_editor_property('key_name', u.Name(name)); return k
try:
    contexts=['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/Input/IMC_Default']
    actions={n:u.load_asset('/Game/VehicleTemplate/Input/Actions/'+n) for n in ['IA_Throttle','IA_Brake','IA_Steering','IA_Handbrake']}
    for ctx_path in contexts:
        ctx=u.load_asset(ctx_path)
        vals=[]
        if not ctx:
            r[ctx_path]='missing'; continue
        ctx.modify()
        try: ctx.unmap_all(); vals.append('unmap_all ok')
        except Exception as e: vals.append('unmap_all ERR '+str(e))
        for act_name, keys in {
            'IA_Throttle':['W','Up','Gamepad_RightTriggerAxis'],
            'IA_Brake':['S','Down','Gamepad_LeftTriggerAxis'],
            'IA_Steering':['A','D','Left','Right','Gamepad_LeftX'],
            'IA_Handbrake':['SpaceBar','Gamepad_FaceButton_Bottom']
        }.items():
            act=actions[act_name]
            for kn in keys:
                try:
                    m=ctx.map_key(act,key(kn)); vals.append(f'{act_name}->{kn}:{m.get_editor_property("key").export_text()}')
                except Exception as e: vals.append(f'{act_name}->{kn} ERR {e}')
        u.EditorAssetLibrary.save_loaded_asset(ctx,False)
        # report data
        try: vals.append('default='+str(ctx.get_editor_property('default_key_mappings').to_dict())[:3000])
        except Exception as e: vals.append('read default ERR '+str(e))
        r[ctx_path]=vals
except Exception:
    r={'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'repair_imc_keys_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
