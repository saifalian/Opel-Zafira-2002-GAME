import unreal as u, pathlib, json, traceback, math
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
r={}
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraStraight5KM')
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label().startswith('S5_StartChaseCamera'):
            u.EditorLevelLibrary.destroy_actor(a)
    cam=u.EditorLevelLibrary.spawn_actor_from_class(u.CameraActor,u.Vector(-900,0,650),u.Rotator(-12,0,0))
    cam.set_actor_label('S5_StartChaseCamera_AutoPlayer0')
    try: cam.set_editor_property('auto_activate_for_player', u.AutoReceiveInput.PLAYER0)
    except Exception as e: r['auto_camera_warning']=str(e)
    comp=cam.get_component_by_class(u.CameraComponent)
    if comp:
        comp.set_field_of_view(82)
        try: comp.set_editor_property('auto_activate', True)
        except Exception: pass
    # raise start/car in case camera was inside collision/ground
    for a in u.EditorLevelLibrary.get_all_level_actors():
        lab=a.get_actor_label()
        if lab.startswith('S5_DrivableZafira'):
            a.set_actor_location(u.Vector(900,0,165),False,False); a.set_actor_rotation(u.Rotator(0,0,0),False)
        if isinstance(a,u.PlayerStart):
            a.set_actor_location(u.Vector(600,0,280),False,False); a.set_actor_rotation(u.Rotator(0,0,0),False)
    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(),'/Game/Zafira/Maps/ZafiraStraight5KM')
    r.update({'success':bool(ok),'camera':'-900,0,650 rot -12,0,0 fov82','purpose':'force visible view of sunny straight road and side scenery'})
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'force_visible_straight_camera_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
