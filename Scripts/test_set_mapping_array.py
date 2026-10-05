import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')

def key(name):
    k=u.Key(); k.set_editor_property('key_name',u.Name(name)); return k
out={}
try:
    neg=u.load_asset('/Game/VehicleTemplate/Input/ZafiraInputNegate_Test') or u.AssetToolsHelpers.get_asset_tools().create_asset('ZafiraInputNegate_Test','/Game/VehicleTemplate/Input',u.InputModifierNegate,None)
    act_steer=u.load_asset('/Game/VehicleTemplate/Input/Actions/IA_Steering')
    for ctx_path in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default']:
        ctx=u.load_asset(ctx_path); ctx.modify(); ctx.unmap_all()
        m=ctx.map_key(act_steer,key('A'))
        data=ctx.get_editor_property('default_key_mappings')
        arr=data.get_editor_property('mappings')
        rows=[]
        rows.append('arr len '+str(len(arr)))
        for i,x in enumerate(arr):
            rows.append('before '+x.export_text())
            mods=x.get_editor_property('modifiers'); mods.append(neg); x.set_editor_property('modifiers',mods)
            arr[i]=x
            rows.append('after '+x.export_text())
        data.set_editor_property('mappings',arr)
        try: ctx.set_editor_property('default_key_mappings',data); rows.append('set data ok')
        except Exception as e: rows.append('set data ERR '+str(e))
        u.EditorAssetLibrary.save_loaded_asset(ctx,False)
        rows.append('verify '+str([mm.export_text() for mm in ctx.get_editor_property('default_key_mappings').get_editor_property('mappings')]))
        out[ctx_path]=rows
except Exception: out={'error':traceback.format_exc()}
(S/'test_set_mapping_array_report.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out))
