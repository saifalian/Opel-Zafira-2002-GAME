import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
out={}
try:
    for bp_path in ['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase','/Game/Zafira/BP_Zafira']:
        bp=u.load_asset(bp_path); ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
        data={}
        for h in ss.k2_gather_subobject_data_for_blueprint(bp):
            obj=lib.get_object(lib.get_data(h))
            if 'VehicleMovement' in obj.get_name() or isinstance(obj,u.ChaosWheeledVehicleMovementComponent):
                entry={'class':obj.get_class().get_name()}
                for p in ['wheel_setups','wheels','mass','drag_coefficient','chassis_width','chassis_height','drag_area','reverse_as_brake']:
                    try: entry[p]=str(obj.get_editor_property(p))[:2000]
                    except Exception as e: entry[p]='ERR '+str(e)
                data[obj.get_name()]=entry
        out[bp_path]=data
except Exception: out={'error':traceback.format_exc()}
(S/'vehicle_movement_base_props.json').write_text(json.dumps(out,indent=2,default=str)); print(S/'vehicle_movement_base_props.json')
