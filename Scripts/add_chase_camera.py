import unreal as u, pathlib, json, traceback
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive'); S=R/'Scripts'; E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
base='/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase'; car='/Game/Zafira/BP_Zafira'
r={}
try:
    bp=u.load_asset(base); z=u.load_asset(car)
    ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
    handles=ss.k2_gather_subobject_data_for_blueprint(bp)
    objs={lib.get_object(lib.get_data(h)).get_name():h for h in handles}
    root=handles[0]
    arm_name=next((n for n in objs if n.startswith('BackSpringArm')),None)
    if arm_name: arm_h=objs[arm_name]
    else:
        arm_h,reason=ss.add_new_subobject(u.AddNewSubobjectParams(parent_handle=root,new_class=u.SpringArmComponent,blueprint_context=bp)); assert not str(reason),str(reason); ss.rename_subobject(arm_h,'BackSpringArm')
    handles=ss.k2_gather_subobject_data_for_blueprint(bp); objs={lib.get_object(lib.get_data(h)).get_name():h for h in handles}
    arm_name=next((n for n in objs if n.startswith('BackSpringArm')),None); assert arm_name, list(objs)
    arm_h=objs[arm_name]
    cam_name=next((n for n in objs if n.startswith('BackCamera')),None)
    if cam_name: cam_h=objs[cam_name]
    else:
        cam_h,reason=ss.add_new_subobject(u.AddNewSubobjectParams(parent_handle=arm_h,new_class=u.CameraComponent,blueprint_context=bp)); assert not str(reason),str(reason); ss.rename_subobject(cam_h,'BackCamera')
    handles=ss.k2_gather_subobject_data_for_blueprint(bp)
    changed=[]
    for h in handles:
        o=lib.get_object(lib.get_data(h)); name=o.get_name()
        if name.startswith('BackSpringArm') and isinstance(o,u.SpringArmComponent):
            o.modify(); o.set_editor_property('relative_location',u.Vector(-180,0,260)); o.set_editor_property('relative_rotation',u.Rotator(-10,0,0)); o.set_editor_property('target_arm_length',1650.0); o.set_editor_property('socket_offset',u.Vector(0,0,180)); o.set_editor_property('do_collision_test',False); o.set_editor_property('use_pawn_control_rotation',False); o.set_editor_property('inherit_pitch',False); o.set_editor_property('inherit_yaw',True); o.set_editor_property('inherit_roll',False); changed.append(name)
        if name.startswith('BackCamera') and isinstance(o,u.CameraComponent):
            o.modify(); o.set_editor_property('field_of_view',82.0); o.set_editor_property('auto_activate',True); o.set_editor_property('use_pawn_control_rotation',False); changed.append(name)
    L.compile_blueprint(bp); L.compile_blueprint(z)
    E.save_loaded_asset(bp,False); E.save_loaded_asset(z,False)
    r={'success':True,'changed':changed}
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'add_chase_camera_report.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,default=str))
assert r.get('success'), r