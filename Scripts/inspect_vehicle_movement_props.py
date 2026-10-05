import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
out={}
try:
    bp=u.load_asset('/Game/Zafira/BP_Zafira')
    ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
    for h in ss.k2_gather_subobject_data_for_blueprint(bp):
        obj=lib.get_object(lib.get_data(h))
        if isinstance(obj,u.ChaosWheeledVehicleMovementComponent):
            data={}
            for prop in dir(obj):
                if any(s in prop.lower() for s in ['wheel','steer','differ','torque','mass','center','trans','gear','brake','engine']):
                    try:
                        val=obj.get_editor_property(prop)
                        data[prop]=str(val)[:1000]
                    except Exception:
                        pass
            out[obj.get_name()]=data
except Exception:
    out={'error':traceback.format_exc()}
(S/'vehicle_movement_props.json').write_text(json.dumps(out,indent=2,default=str)); print(S/'vehicle_movement_props.json')
