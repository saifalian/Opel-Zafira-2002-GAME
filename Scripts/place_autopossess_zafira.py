import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
r={}
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraStraight5KM')
    # remove any manually placed zafira start actors from previous attempts
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label().startswith('S5_DrivableZafira'):
            u.EditorLevelLibrary.destroy_actor(a)
    pawn_cls=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira')
    car=u.EditorLevelLibrary.spawn_actor_from_class(pawn_cls,u.Vector(900,0,120),u.Rotator(0,0,0))
    car.set_actor_label('S5_DrivableZafira_Player0')
    try: car.set_editor_property('auto_possess_player', u.AutoReceiveInput.PLAYER0)
    except Exception as e: r['auto_possess_warning']=str(e)
    try: car.set_editor_property('auto_receive_input', u.AutoReceiveInput.PLAYER0)
    except Exception: pass
    # keep PlayerStart nearby but not colliding
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if isinstance(a,u.PlayerStart):
            a.set_actor_location(u.Vector(600,0,230),False,False); a.set_actor_rotation(u.Rotator(0,0,0),False)
    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(),'/Game/Zafira/Maps/ZafiraStraight5KM')
    r.update({'success':bool(ok),'placed_car':car.get_actor_label(),'location':'900,0,120','auto_possess':'PLAYER0'})
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'place_autopossess_zafira_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
