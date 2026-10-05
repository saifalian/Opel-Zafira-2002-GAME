import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
report={}
try:
    # restore Zafira game mode for the new clear/visible map
    for gm_path in ['/Game/Zafira/BP_ZafiraGameMode','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode']:
        gm=E.load_asset(gm_path); cls=E.load_blueprint_class(gm_path); cdo=u.get_default_object(cls); cdo.modify()
        zcls=E.load_blueprint_class('/Game/Zafira/BP_Zafira')
        pccls=E.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
        if zcls: cdo.set_editor_property('default_pawn_class', zcls)
        if pccls: cdo.set_editor_property('player_controller_class', pccls)
        L.compile_blueprint(gm); E.save_loaded_asset(gm,False)
    # set playable map world settings to ZafiraGameMode
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraPlayableTrack')
    world=u.EditorLevelLibrary.get_editor_world(); ws=world.get_world_settings(); ws.modify()
    gmcls=E.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode') or E.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode')
    ws.set_editor_property('default_game_mode', gmcls)
    # move PlayerStart a bit above road to avoid collision
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart':
            a.set_actor_location(u.Vector(-650,0,380),False,False); a.set_actor_rotation(u.Rotator(0,0,0),False)
    ok1=u.EditorLoadingAndSavingUtils.save_dirty_packages(True,True); ok2=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraPlayableTrack')
    report={'success':True,'save_dirty':ok1,'save_map':ok2,'gm':str(gmcls)}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'enable_zafira_on_playable_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')