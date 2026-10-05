import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
r={}
try:
    pawn=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira')
    pc=u.EditorAssetLibrary.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
    gm_paths=['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode','/Game/Zafira/BP_ZafiraGameMode']
    for gp in gm_paths:
        bp=u.load_asset(gp); cls=u.EditorAssetLibrary.load_blueprint_class(gp); cdo=u.get_default_object(cls); vals={}
        for prop,val in [('default_pawn_class',pawn),('player_controller_class',pc)]:
            try:
                before=str(cdo.get_editor_property(prop)); cdo.set_editor_property(prop,val); vals[prop]=[before,str(cdo.get_editor_property(prop))]
            except Exception as e: vals[prop]='ERR '+str(e)
        u.BlueprintEditorLibrary.compile_blueprint(bp); u.EditorAssetLibrary.save_loaded_asset(bp,False); r[gp]=vals
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraStraight5KM')
    ws=u.EditorLevelLibrary.get_editor_world().get_world_settings(); ws.modify(); ws.set_editor_property('default_game_mode',u.EditorAssetLibrary.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode'))
    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(),'/Game/Zafira/Maps/ZafiraStraight5KM')
    r['map_saved']=bool(ok)
except Exception:
    r={'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'fix_gamemode_default_pawn_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
