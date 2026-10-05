import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')

def key(name):
    k=u.Key(); k.set_editor_property('key_name', u.Name(name)); return k

def add(ctx, act, kn, neg=False):
    m=ctx.map_key(act,key(kn))
    if neg:
        # Named instanced modifier with the mapping context as outer, so it can be serialized into the .uasset.
        mod=u.new_object(u.InputModifierNegate, outer=ctx, name='InputModifierNegate_'+kn)
        mods=m.get_editor_property('modifiers'); mods.append(mod); m.set_editor_property('modifiers', mods)
    return m.export_text()

out={}
try:
    actions={n:u.load_asset('/Game/VehicleTemplate/Input/Actions/'+n) for n in ['IA_Throttle','IA_Brake','IA_Steering','IA_Handbrake','IA_Reset','IA_ToggleCamera']}
    for ctx_path in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/VehicleTemplate/Input/IMC_SteeringWheel','/Game/Input/IMC_Default']:
        ctx=u.load_asset(ctx_path); ctx.modify(); ctx.unmap_all(); rows=[]
        rows.append(add(ctx,actions['IA_Throttle'],'W'))
        rows.append(add(ctx,actions['IA_Throttle'],'Up'))
        rows.append(add(ctx,actions['IA_Brake'],'S'))
        rows.append(add(ctx,actions['IA_Brake'],'Down'))
        rows.append(add(ctx,actions['IA_Steering'],'A',True))
        rows.append(add(ctx,actions['IA_Steering'],'Left',True))
        rows.append(add(ctx,actions['IA_Steering'],'D'))
        rows.append(add(ctx,actions['IA_Steering'],'Right'))
        rows.append(add(ctx,actions['IA_Handbrake'],'SpaceBar'))
        if ctx_path.endswith('IMC_SteeringWheel'):
            rows.append(add(ctx,actions['IA_Reset'],'R'))
            rows.append(add(ctx,actions['IA_ToggleCamera'],'C'))
        u.EditorAssetLibrary.save_loaded_asset(ctx,False)
        # reload and verify serialized modifiers
        u.EditorAssetLibrary.save_loaded_asset(ctx,False)
        maps=ctx.get_editor_property('default_key_mappings').get_editor_property('mappings')
        out[ctx_path]={'written':rows,'verify':[m.export_text() for m in maps]}
except Exception:
    out={'error':traceback.format_exc()}; u.log_error(out['error'])
(S/'repair_persistent_negate_report.json').write_text(json.dumps(out,indent=2,default=str)); print(json.dumps(out,default=str))
