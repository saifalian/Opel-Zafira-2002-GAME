import unreal as u, pathlib, json, traceback, math
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive'); S=R/'Scripts'
report={}
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraLongTrack')
    world=u.EditorLevelLibrary.get_editor_world()
    # remove already placed zafira pawns/vehicles that can block GameMode spawn
    removed=[]
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        n=a.get_name().lower(); cls=a.get_class().get_name().lower()
        if ('zafira' in n or 'vehicle' in n or 'pawn' in cls or 'chaoswheeledvehicle' in cls) and 'playerstart' not in n:
            try:
                removed.append(a.get_name()); u.EditorLevelLibrary.destroy_actor(a)
            except Exception: pass
    # find or create PlayerStart high above clear track; use exact log location but much higher
    starts=[a for a in u.EditorLevelLibrary.get_all_level_actors() if a.get_class().get_name()=='PlayerStart']
    ps=starts[0] if starts else u.EditorLevelLibrary.spawn_actor_from_class(u.PlayerStart, u.Vector(84724.0,-163.0,2200.0), u.Rotator(0,0,0))
    ps.set_actor_location(u.Vector(84724.0,-163.0,2200.0), False, False)
    ps.set_actor_rotation(u.Rotator(-8,0,0), False)
    # make a large visible platform/road below spawn so falling/spawn is obvious
    mat_path='/Game/Zafira/LongTrack/M_PC_Unlit_Road'
    mat=u.load_asset(mat_path)
    if not mat:
        mat=u.AssetToolsHelpers.get_asset_tools().create_asset('M_PC_Unlit_Road','/Game/Zafira/LongTrack',u.Material,u.MaterialFactoryNew())
        mat.set_editor_property('shading_model', u.MaterialShadingModel.MSM_UNLIT)
        mat.set_editor_property('blend_mode', u.BlendMode.BLEND_OPAQUE)
    cube=u.load_asset('/Engine/BasicShapes/Cube.Cube')
    for name,loc,scale in [
        ('PC_Spawn_Bright_Road',u.Vector(84724,-163,1000),u.Vector(70,18,1)),
        ('PC_Spawn_Green_Left',u.Vector(84724,-2200,995),u.Vector(70,8,1)),
        ('PC_Spawn_Green_Right',u.Vector(84724,1900,995),u.Vector(70,8,1))]:
        old=[a for a in u.EditorLevelLibrary.get_all_level_actors() if a.get_name().startswith(name)]
        for a in old: u.EditorLevelLibrary.destroy_actor(a)
        a=u.EditorLevelLibrary.spawn_actor_from_object(cube,loc,u.Rotator(0,0,0)); a.set_actor_label(name); a.set_actor_scale3d(scale)
        if mat and hasattr(a,'static_mesh_component'): a.static_mesh_component.set_material(0,mat)
    u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    report={'success':True,'removed':removed,'playerstart':[84724,-163,2200],'note':'Raised PlayerStart far above collision and removed blocking placed vehicle/pawn actors.'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'fix_spawn_high_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))
assert report.get('success'), report