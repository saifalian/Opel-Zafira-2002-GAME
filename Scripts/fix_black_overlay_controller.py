import unreal as u, pathlib, json, traceback
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive'); S=R/'Scripts'; E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
report={}
try:
    bp=E.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode')
    cls=E.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode')
    cdo=u.get_default_object(cls); cdo.modify()
    # Use default PlayerController only to remove template HUD/black overlay logic; keep Zafira pawn.
    cdo.set_editor_property('player_controller_class', u.PlayerController.static_class())
    zcls=E.load_blueprint_class('/Game/Zafira/BP_Zafira')
    if zcls: cdo.set_editor_property('default_pawn_class', zcls)
    L.compile_blueprint(bp); E.save_loaded_asset(bp,False)
    # Also make Zafira-specific game mode inherit same safe controller.
    zgm=E.load_asset('/Game/Zafira/BP_ZafiraGameMode')
    zgmc=E.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode')
    if zgmc:
        zcdo=u.get_default_object(zgmc); zcdo.modify(); zcdo.set_editor_property('player_controller_class', u.PlayerController.static_class())
        if zcls: zcdo.set_editor_property('default_pawn_class', zcls)
        L.compile_blueprint(zgm); E.save_loaded_asset(zgm,False)
    report={'success':True,'change':'Disabled custom VehicleAdvPlayerController HUD/overlay by switching GameMode to default PlayerController; kept BP_Zafira pawn.'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'fix_black_overlay_controller_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))
assert report.get('success'), report