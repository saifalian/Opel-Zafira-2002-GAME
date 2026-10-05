import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')

def key(name):
    k=u.Key(); k.set_editor_property('key_name',u.Name(name)); return k

def ensure_asset(name, cls):
    path='/Game/VehicleTemplate/Input/'+name
    obj=u.load_asset(path)
    if not obj:
        obj=u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/VehicleTemplate/Input',cls,None)
        u.EditorAssetLibrary.save_loaded_asset(obj,False)
    return obj

def rebuild(ctx_path, entries):
    ctx=u.load_asset(ctx_path); ctx.modify(); ctx.unmap_all()
    for act,kn in entries:
        ctx.map_key(act, key(kn))
    data=ctx.get_editor_property('default_key_mappings')
    arr=data.get_editor_property('mappings')
    for i,m in enumerate(arr):
        kn=m.get_editor_property('key').export_text()
        if kn in ['A','Left']:
            mods=m.get_editor_property('modifiers'); mods.append(neg); m.set_editor_property('modifiers',mods); arr[i]=m
    data.set_editor_property('mappings',arr)
    ctx.set_editor_property('default_key_mappings',data)
    u.EditorAssetLibrary.save_loaded_asset(ctx,False)
    return [m.export_text() for m in ctx.get_editor_property('default_key_mappings').get_editor_property('mappings')]

out={}
try:
    neg=ensure_asset('ZafiraSteerLeft_NegateAsset', u.InputModifierNegate)
    acts={n:u.load_asset('/Game/VehicleTemplate/Input/Actions/'+n) for n in ['IA_Throttle','IA_Brake','IA_Steering','IA_Handbrake','IA_Reset','IA_ToggleCamera','IA_LookAround','IA_Headlights']}
    base=[(acts['IA_Throttle'],'W'),(acts['IA_Throttle'],'Up'),(acts['IA_Brake'],'S'),(acts['IA_Brake'],'Down'),(acts['IA_Steering'],'A'),(acts['IA_Steering'],'Left'),(acts['IA_Steering'],'D'),(acts['IA_Steering'],'Right'),(acts['IA_Handbrake'],'SpaceBar')]
    out['/Game/VehicleTemplate/Input/IMC_Vehicle_Default']=rebuild('/Game/VehicleTemplate/Input/IMC_Vehicle_Default', base+[(acts['IA_Reset'],'BackSpace'),(acts['IA_ToggleCamera'],'Tab'),(acts['IA_Headlights'],'L')])
    out['/Game/VehicleTemplate/Input/IMC_SteeringWheel']=rebuild('/Game/VehicleTemplate/Input/IMC_SteeringWheel', base+[(acts['IA_Reset'],'R'),(acts['IA_ToggleCamera'],'C')])
    out['/Game/Input/IMC_Default']=rebuild('/Game/Input/IMC_Default', base)
except Exception:
    out={'error':traceback.format_exc()}; u.log_error(out['error'])
(S/'repair_final_keyboard_steering_report.json').write_text(json.dumps(out,indent=2,default=str)); print(json.dumps(out,default=str))
