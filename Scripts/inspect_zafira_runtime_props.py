import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
try:
    bp=u.load_asset('/Game/Zafira/BP_Zafira')
    cls=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira')
    cdo=u.get_default_object(cls)
    out={'props':{},'components':[]}
    for p in ['auto_possess_player','auto_receive_input','input_priority','block_input']:
        try: out['props'][p]=str(cdo.get_editor_property(p))
        except Exception as e: out['props'][p]='ERR '+str(e)
    ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
    for h in ss.k2_gather_subobject_data_for_blueprint(bp):
        o=lib.get_object(lib.get_data(h)); row={'name':o.get_name(),'class':o.get_class().get_name()}
        if 'Movement' in row['class'] or 'Vehicle' in row['class']:
            for p in ['auto_activate','updated_component','max_engine_rpm','engine_setup','transmission_setup','wheel_setups','enable_physics_interaction']:
                try: row[p]=str(o.get_editor_property(p))
                except Exception: pass
        out['components'].append(row)
    (S/'zafira_runtime_props.json').write_text(json.dumps(out,indent=2,default=str))
except Exception:
    (S/'zafira_runtime_props.json').write_text(json.dumps({'error':traceback.format_exc()},indent=2))
print(S/'zafira_runtime_props.json')