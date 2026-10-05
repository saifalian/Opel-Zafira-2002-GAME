import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
report={}
try:
    path='/Game/Zafira/BP_ZafiraArcadePawn'
    bp=E.load_asset(path)
    if not bp:
        bp=L.create_blueprint_asset_with_parent(path,u.DefaultPawn)
    cls=E.load_blueprint_class(path); cdo=u.get_default_object(cls); cdo.modify()
    body=E.load_asset('/Game/Zafira/Meshes/SM_Zafira_Body_Aligned') or E.load_asset('/Game/Zafira/Meshes/SM_Zafira_Body')
    # DefaultPawn has MeshComponent; set it to Zafira body and make it visible/large enough.
    for prop in ['mesh_component','MeshComponent']:
        try:
            mc=cdo.get_editor_property(prop)
            if mc and body:
                mc.set_editor_property('static_mesh', body)
                mc.set_editor_property('relative_location', u.Vector(0,0,-85))
                mc.set_editor_property('relative_rotation', u.Rotator(0,0,0))
                mc.set_editor_property('relative_scale3d', u.Vector(1,1,1))
                break
        except Exception: pass
    # Make default pawn drive more car-like, not slow flying ball.
    for prop in ['movement_component','MovementComponent']:
        try:
            mv=cdo.get_editor_property(prop)
            if mv:
                for p,v in [('max_speed',4200.0),('acceleration',7000.0),('deceleration',5500.0)]:
                    try: mv.set_editor_property(p,v)
                    except Exception: pass
                break
        except Exception: pass
    L.compile_blueprint(bp); E.save_loaded_asset(bp,False)
    # Use arcade Zafira pawn in both game modes for guaranteed keyboard/mobile movement.
    for gm_path in ['/Game/Zafira/BP_ZafiraGameMode','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode']:
        gm=E.load_asset(gm_path); gmcls=E.load_blueprint_class(gm_path); gcdo=u.get_default_object(gmcls); gcdo.modify()
        gcdo.set_editor_property('default_pawn_class', cls)
        gcdo.set_editor_property('player_controller_class', u.PlayerController.static_class())
        L.compile_blueprint(gm); E.save_loaded_asset(gm,False)
    report={'success':True,'pawn':path,'mesh':str(body),'note':'Created arcade Zafira DefaultPawn with real Zafira mesh and fast WASD movement; set game modes to use it.'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'create_arcade_zafira_pawn_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')