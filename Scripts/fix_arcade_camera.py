import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
r={}
try:
    bp=E.load_asset('/Game/Zafira/BP_ZafiraArcadePawn'); cls=E.load_blueprint_class('/Game/Zafira/BP_ZafiraArcadePawn'); cdo=u.get_default_object(cls); cdo.modify()
    # Ensure mesh is visible to owner and placed where chase camera sees it.
    for prop in ['mesh_component','MeshComponent']:
        try:
            mc=cdo.get_editor_property(prop)
            if mc:
                mc.set_editor_property('hidden_in_game', False)
                try: mc.set_editor_property('owner_no_see', False)
                except Exception: pass
                mc.set_editor_property('relative_location', u.Vector(120,0,-95))
                mc.set_editor_property('relative_rotation', u.Rotator(0,0,0))
                mc.set_editor_property('relative_scale3d', u.Vector(1,1,1))
        except Exception: pass
    ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
    handles=ss.k2_gather_subobject_data_for_blueprint(bp); root=handles[0]
    objs={lib.get_object(lib.get_data(h)).get_name():h for h in handles}
    arm_h=objs.get('ArcadeChaseArm')
    if not arm_h:
        arm_h,reason=ss.add_new_subobject(u.AddNewSubobjectParams(parent_handle=root,new_class=u.SpringArmComponent,blueprint_context=bp)); assert not str(reason),str(reason); ss.rename_subobject(arm_h,'ArcadeChaseArm')
    handles=ss.k2_gather_subobject_data_for_blueprint(bp); objs={lib.get_object(lib.get_data(h)).get_name():h for h in handles}; arm_h=next((h for name,h in objs.items() if name.startswith('ArcadeChaseArm')), None)
    cam_h=next((h for name,h in objs.items() if name.startswith('ArcadeChaseCamera')), None)
    if not cam_h:
        cam_h,reason=ss.add_new_subobject(u.AddNewSubobjectParams(parent_handle=arm_h,new_class=u.CameraComponent,blueprint_context=bp)); assert not str(reason),str(reason); ss.rename_subobject(cam_h,'ArcadeChaseCamera')
    handles=ss.k2_gather_subobject_data_for_blueprint(bp); changed=[]
    for h in handles:
        o=lib.get_object(lib.get_data(h)); n=o.get_name()
        if n.startswith('ArcadeChaseArm') and isinstance(o,u.SpringArmComponent):
            o.modify(); o.set_editor_property('target_arm_length',900.0); o.set_editor_property('relative_location',u.Vector(0,0,180)); o.set_editor_property('relative_rotation',u.Rotator(-12,0,0)); o.set_editor_property('socket_offset',u.Vector(0,0,80)); o.set_editor_property('do_collision_test',False); changed.append(n)
        if n.startswith('ArcadeChaseCamera') and isinstance(o,u.CameraComponent):
            o.modify(); o.set_editor_property('auto_activate',True); o.set_editor_property('field_of_view',82.0); changed.append(n)
    L.compile_blueprint(bp); E.save_loaded_asset(bp,False)
    r={'success':True,'changed':changed}
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'fix_arcade_camera_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
assert r.get('success')