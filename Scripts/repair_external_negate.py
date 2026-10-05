import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')

def key(name):
    k=u.Key(); k.set_editor_property('key_name',u.Name(name)); return k

def make_neg_asset(name):
    path='/Game/VehicleTemplate/Input/'+name
    obj=u.load_asset(path)
    if not obj:
        obj=u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/VehicleTemplate/Input',u.InputModifierNegate,None)
    if obj: u.EditorAssetLibrary.save_loaded_asset(obj,False)
    return obj

def add(ctx,act,kn,mods=None):
    m=ctx.map_key(act,key(kn))
    if mods:
        arr=m.get_editor_property('modifiers')
        for mod in mods: arr.append(mod)
        m.set_editor_property('modifiers',arr)
    return m.export_text()

out={}
try:
    neg_left=make_neg_asset('ZafiraSteerLeft_Negate')
    neg_a=make_neg_asset('ZafiraSteerA_Negate')
    actions={n:u.load_asset('/Game/VehicleTemplate/Input/Actions/'+n) for n in ['IA_Throttle','IA_Brake','IA_Steering','IA_Handbrake','IA_Reset','IA_ToggleCamera']}
    for ctx_path in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/VehicleTemplate/Input/IMC_SteeringWheel','/Game/Input/IMC_Default']:
        ctx=u.load_asset(ctx_path); ctx.modify(); ctx.unmap_all(); rows=[]
        for act,kn,mods in [
            ('IA_Throttle','W',None),('IA_Throttle','Up',None),
            ('IA_Brake','S',None),('IA_Brake','Down',None),
            ('IA_Steering','A',[neg_a]),('IA_Steering','Left',[neg_left]),
            ('IA_Steering','D',None),('IA_Steering','Right',None),
            ('IA_Handbrake','SpaceBar',None)]:
            rows.append(add(ctx,actions[act],kn,mods))
        if ctx_path.endswith('IMC_SteeringWheel'):
            rows.append(add(ctx,actions['IA_Reset'],'R'))
            rows.append(add(ctx,actions['IA_ToggleCamera'],'C'))
        u.EditorAssetLibrary.save_loaded_asset(ctx,False)
        maps=ctx.get_editor_property('default_key_mappings').get_editor_property('mappings')
        out[ctx_path]={'verify':[m.export_text() for m in maps]}
except Exception:
    out={'error':traceback.format_exc()}; u.log_error(out['error'])
(S/'repair_external_negate_report.json').write_text(json.dumps(out,indent=2,default=str)); print(json.dumps(out,default=str))
