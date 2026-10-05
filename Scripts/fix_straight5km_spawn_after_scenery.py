import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
MAP='/Game/Zafira/Maps/ZafiraStraight5KM'
r={}
try:
    u.EditorLoadingAndSavingUtils.load_map(MAP)
    ws=u.EditorLevelLibrary.get_editor_world().get_world_settings()
    gm=u.EditorAssetLibrary.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode')
    ws.modify(); ws.set_editor_property('default_game_mode', gm)
    # ensure player start open center lane
    found=False
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if isinstance(a,u.PlayerStart):
            a.set_actor_label('S5_PlayerStart')
            a.set_actor_location(u.Vector(700,0,180),False,False)
            a.set_actor_rotation(u.Rotator(0,0,0),False)
            found=True
    if not found:
        ps=u.EditorLevelLibrary.spawn_actor_from_class(u.PlayerStart,u.Vector(700,0,180),u.Rotator(0,0,0)); ps.set_actor_label('S5_PlayerStart')
    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(),MAP)
    r={'success':bool(ok),'map':MAP,'game_mode':'/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode','player_start':'700,0,180'}
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'fix_straight5km_spawn_after_scenery_report.json').write_text(json.dumps(r,indent=2)); print(json.dumps(r))
