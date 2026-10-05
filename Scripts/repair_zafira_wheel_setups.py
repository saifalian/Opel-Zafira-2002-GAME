import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
out={}
try:
    front=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_WheelsFront')
    rear=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_WheelsRear')
    setups=[]
    for cls,bone in [(front,'Phys_Wheel_FL'),(front,'Phys_Wheel_FR'),(rear,'Phys_Wheel_BL'),(rear,'Phys_Wheel_BR')]:
        w=u.ChaosWheelSetup()
        w.set_editor_property('wheel_class', cls)
        w.set_editor_property('bone_name', u.Name(bone))
        w.set_editor_property('additional_offset', u.Vector(0,0,0))
        setups.append(w)
    for bp_path in ['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase','/Game/Zafira/BP_Zafira']:
        bp=u.load_asset(bp_path); ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
        rows=[]
        for h in ss.k2_gather_subobject_data_for_blueprint(bp):
            obj=lib.get_object(lib.get_data(h))
            if isinstance(obj,u.ChaosWheeledVehicleMovementComponent):
                obj.modify()
                before=[x.export_text() for x in obj.get_editor_property('wheel_setups')]
                obj.set_editor_property('wheel_setups', setups)
                obj.set_use_automatic_gears(True)
                obj.set_target_gear(1, True)
                obj.set_requires_controller_for_inputs(False)
                obj.set_editor_property('reverse_as_brake', True)
                after=[x.export_text() for x in obj.get_editor_property('wheel_setups')]
                rows.append({'component':obj.get_name(),'before':before,'after':after})
        u.BlueprintEditorLibrary.compile_blueprint(bp); u.EditorAssetLibrary.save_loaded_asset(bp,False)
        out[bp_path]=rows
except Exception:
    out={'error':traceback.format_exc()}; u.log_error(out['error'])
(S/'repair_zafira_wheel_setups_report.json').write_text(json.dumps(out,indent=2,default=str)); print(json.dumps(out,default=str))
