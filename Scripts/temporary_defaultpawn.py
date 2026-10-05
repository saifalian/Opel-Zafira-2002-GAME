import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
report={}
try:
    for path in ['/Game/Zafira/BP_ZafiraGameMode','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode']:
        bp=E.load_asset(path); cls=E.load_blueprint_class(path); cdo=u.get_default_object(cls); cdo.modify()
        cdo.set_editor_property('player_controller_class', u.PlayerController.static_class())
        cdo.set_editor_property('default_pawn_class', u.DefaultPawn.static_class())
        cdo.set_editor_property('hud_class', None)
        L.compile_blueprint(bp); E.save_loaded_asset(bp,False)
    report={'success':True,'change':'Temporarily set GameModes to DefaultPawn/default PlayerController/no HUD so map renders instead of failed BP_Zafira spawn black screen.'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'temporary_defaultpawn_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report))
assert report.get('success')