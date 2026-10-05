import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
report={}
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraLongTrack')
    world=u.EditorLevelLibrary.get_editor_world()
    # Remove old forced cameras/platform copies
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label().startswith('FORCED_VISIBLE_') or a.get_name().startswith('FORCED_VISIBLE_'):
            u.EditorLevelLibrary.destroy_actor(a)
    # Big unlit bright visual target in front of camera
    cube=u.load_asset('/Engine/BasicShapes/Cube.Cube')
    mat=u.load_asset('/Game/Zafira/LongTrack/M_PC_Unlit_Road')
    if not mat:
        mat=u.AssetToolsHelpers.get_asset_tools().create_asset('M_PC_Unlit_Road','/Game/Zafira/LongTrack',u.Material,u.MaterialFactoryNew())
        mat.set_editor_property('shading_model', u.MaterialShadingModel.MSM_UNLIT)
    items=[
        ('FORCED_VISIBLE_GREY_ROAD', u.Vector(2000,0,0), u.Vector(80,18,1)),
        ('FORCED_VISIBLE_GREEN_LEFT', u.Vector(2000,-2500,-10), u.Vector(80,8,1)),
        ('FORCED_VISIBLE_GREEN_RIGHT', u.Vector(2000,2500,-10), u.Vector(80,8,1)),
        ('FORCED_VISIBLE_RED_WALL', u.Vector(5500,-1100,300), u.Vector(2,2,8)),
        ('FORCED_VISIBLE_YELLOW_WALL', u.Vector(5500,1100,300), u.Vector(2,2,8)),
    ]
    made=[]
    for name,loc,scale in items:
        a=u.EditorLevelLibrary.spawn_actor_from_object(cube,loc,u.Rotator(0,0,0)); a.set_actor_label(name); a.set_actor_scale3d(scale); made.append(name)
        if mat and hasattr(a,'static_mesh_component'): a.static_mesh_component.set_material(0,mat)
    # Put camera looking straight at target; auto-activate for player 0 so no pawn is needed
    cam=u.EditorLevelLibrary.spawn_actor_from_class(u.CameraActor, u.Vector(-1600,0,800), u.Rotator(-12,0,0))
    cam.set_actor_label('FORCED_VISIBLE_PLAYER_CAMERA')
    try: cam.set_editor_property('auto_activate_for_player', u.AutoReceiveInput.PLAYER0)
    except Exception: pass
    cc=cam.get_editor_property('camera_component')
    cc.set_editor_property('field_of_view', 80.0)
    # Add directional light if none visible
    light=u.EditorLevelLibrary.spawn_actor_from_class(u.DirectionalLight, u.Vector(0,0,4000), u.Rotator(-45,25,0)); light.set_actor_label('FORCED_VISIBLE_SUN')
    try: light.get_editor_property('light_component').set_editor_property('intensity', 8.0)
    except Exception: pass
    # World settings: no custom GM, no HUD needed for validation
    ws=world.get_world_settings(); ws.modify(); ws.set_editor_property('default_game_mode', u.GameModeBase.static_class())
    # Persist map and assets
    ok_dirty=u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    ok_asset=u.EditorAssetLibrary.save_asset('/Game/Zafira/Maps/ZafiraLongTrack', False)
    report={'success':True,'actors':made+['FORCED_VISIBLE_PLAYER_CAMERA','FORCED_VISIBLE_SUN'],'save_dirty':ok_dirty,'save_asset':ok_asset}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'force_visible_camera_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')