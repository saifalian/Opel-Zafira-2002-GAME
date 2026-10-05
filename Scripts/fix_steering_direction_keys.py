import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')

def key(name):
    k=u.Key(); k.set_editor_property('key_name', u.Name(name)); return k

def add_mapping(ctx, action, key_name, negate=False):
    m=ctx.map_key(action, key(key_name))
    if negate:
        try:
            mod=u.new_object(u.InputModifierNegate, ctx)
            mods=m.get_editor_property('modifiers')
            mods.append(mod)
            m.set_editor_property('modifiers', mods)
        except Exception as e:
            return f'{action.get_name()}->{key_name} NEGATE_ERR {e}'
    try:
        mods=m.get_editor_property('modifiers')
        return f'{action.get_name()}->{key_name} key={m.get_editor_property("key").export_text()} mods={[x.get_class().get_name() for x in mods]}'
    except Exception as e:
        return f'{action.get_name()}->{key_name} READ_ERR {e}'

out={}
try:
    actions={n:u.load_asset('/Game/VehicleTemplate/Input/Actions/'+n) for n in ['IA_Throttle','IA_Brake','IA_Steering','IA_Handbrake']}
    for ctx_path in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/Input/IMC_Default']:
        ctx=u.load_asset(ctx_path)
        if not ctx:
            out[ctx_path]='missing'; continue
        ctx.modify()
        rows=[]
        try: ctx.unmap_all(); rows.append('unmap_all ok')
        except Exception as e: rows.append('unmap_all ERR '+str(e))
        # Keyboard only first, to remove accidental stuck/right gamepad axis while debugging.
        rows.append(add_mapping(ctx, actions['IA_Throttle'], 'W', False))
        rows.append(add_mapping(ctx, actions['IA_Throttle'], 'Up', False))
        rows.append(add_mapping(ctx, actions['IA_Brake'], 'S', False))
        rows.append(add_mapping(ctx, actions['IA_Brake'], 'Down', False))
        rows.append(add_mapping(ctx, actions['IA_Steering'], 'A', True))
        rows.append(add_mapping(ctx, actions['IA_Steering'], 'Left', True))
        rows.append(add_mapping(ctx, actions['IA_Steering'], 'D', False))
        rows.append(add_mapping(ctx, actions['IA_Steering'], 'Right', False))
        rows.append(add_mapping(ctx, actions['IA_Handbrake'], 'SpaceBar', False))
        u.EditorAssetLibrary.save_loaded_asset(ctx, False)
        out[ctx_path]=rows
    # keep real Zafira automatic/drive settings
    for bp_path in ['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase','/Game/Zafira/BP_Zafira']:
        bp=u.load_asset(bp_path)
        ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
        vals=[]
        for h in ss.k2_gather_subobject_data_for_blueprint(bp):
            obj=lib.get_object(lib.get_data(h))
            if isinstance(obj, u.ChaosWheeledVehicleMovementComponent):
                obj.modify()
                for call,args in [('set_use_automatic_gears',[True]),('set_target_gear',[1,True]),('set_requires_controller_for_inputs',[False])]:
                    try: getattr(obj,call)(*args); vals.append(call+' ok')
                    except Exception as e: vals.append(call+' ERR '+str(e))
        u.BlueprintEditorLibrary.compile_blueprint(bp); u.EditorAssetLibrary.save_loaded_asset(bp, False)
        out[bp_path]=vals
except Exception:
    out={'error':traceback.format_exc()}; u.log_error(out['error'])
(S/'fix_steering_direction_keys_report.json').write_text(json.dumps(out,indent=2,default=str))
print(json.dumps(out,default=str))
