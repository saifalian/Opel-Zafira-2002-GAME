import unreal as u, pathlib, json
bp=u.load_asset('/Game/Zafira/BP_Zafira'); ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
out=[]
for h in ss.k2_gather_subobject_data_for_blueprint(bp):
    o=lib.get_object(lib.get_data(h))
    if isinstance(o,u.ChaosWheeledVehicleMovementComponent):
        for name in dir(o):
            if any(s in name.lower() for s in ['gear','trans','engine','throttle','brake','input']): out.append(name)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/vehicle_move_api.json'); path.write_text(json.dumps(out,indent=2)); print(path)
