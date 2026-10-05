import unreal as u, pathlib, json, traceback, math
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
SRC=ROOT/'SourceArt/LongTrack'
ASSET_DIR='/Game/Zafira/LongTrack'
MESH_DIR=ASSET_DIR+'/Meshes'
MAT_DIR=ASSET_DIR+'/Materials'
MAP_PATH='/Game/Zafira/Maps/ZafiraLongTrack'
report={'imported':[], 'map':MAP_PATH}
COLORS={
 'LT_Road':(0.018,0.018,0.02), 'LT_Curbs_L':(0.9,0.08,0.06), 'LT_Curbs_R':(0.94,0.94,0.9),
 'LT_Terrain':(0.06,0.35,0.075), 'LT_Barriers':(0.75,0.75,0.78), 'LT_CityBuildings':(0.32,0.34,0.36),
 'LT_Trees':(0.035,0.27,0.06), 'LT_StartGantry':(0.08,0.08,0.09)
}
try:
    meta=json.loads((SRC/'long_track_meta.json').read_text())
    tools=u.AssetToolsHelpers.get_asset_tools()
    tasks=[]
    for obj in sorted(SRC.glob('LT_*.obj')):
        t=u.AssetImportTask(); t.filename=str(obj); t.destination_path=MESH_DIR; t.destination_name=obj.stem
        t.automated=True; t.save=True; t.replace_existing=True
        tasks.append(t)
    tools.import_asset_tasks(tasks)
    def mat(name,color):
        path=f'{MAT_DIR}/M_{name}'
        if u.EditorAssetLibrary.does_asset_exist(path): return u.EditorAssetLibrary.load_asset(path)
        m=tools.create_asset('M_'+name,MAT_DIR,u.Material,u.MaterialFactoryNew())
        base=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-300,100)
        base.constant=u.LinearColor(color[0],color[1],color[2],1)
        u.MaterialEditingLibrary.connect_material_property(base,'RGB',u.MaterialProperty.MP_BASE_COLOR)
        rough=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-300,300); rough.r=.85
        u.MaterialEditingLibrary.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
        u.MaterialEditingLibrary.recompile_material(m); u.EditorAssetLibrary.save_asset(path); return m
    mats={k:mat(k,v) for k,v in COLORS.items()}
    meshes=[]
    for obj in sorted(SRC.glob('LT_*.obj')):
        path=f'{MESH_DIR}/{obj.stem}'
        sm=u.EditorAssetLibrary.load_asset(path); assert sm, path
        if obj.stem in mats:
            try: sm.set_material(0,mats[obj.stem])
            except Exception: pass
        try:
            body=sm.get_editor_property('body_setup')
            if body:
                body.set_editor_property('collision_trace_flag', u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
        except Exception as e: report.setdefault('collision_warnings',[]).append(f'{obj.stem}: {e}')
        u.EditorAssetLibrary.save_asset(path); meshes.append((obj.stem,sm)); report['imported'].append(path)
    world=u.EditorLoadingAndSavingUtils.new_blank_map(False)
    actor_sub=u.get_editor_subsystem(u.EditorActorSubsystem)
    for name,sm in meshes:
        a=actor_sub.spawn_actor_from_class(u.StaticMeshActor,u.Vector(0,0,0),u.Rotator(0,0,0))
        a.set_actor_label(name); a.static_mesh_component.set_static_mesh(sm)
        a.static_mesh_component.set_mobility(u.ComponentMobility.STATIC)
    sx,sy,sz=meta['start']; yaw=meta['start_yaw_deg']
    actor_sub.spawn_actor_from_class(u.PlayerStart,u.Vector(sx,sy,sz+130),u.Rotator(0,yaw,0))
    # extra lights/sky for Android-friendly daylight
    sun=actor_sub.spawn_actor_from_class(u.DirectionalLight,u.Vector(0,0,18000),u.Rotator(-48,25,0)); sun.light_component.set_editor_property('intensity',4.5)
    sky=actor_sub.spawn_actor_from_class(u.SkyLight,u.Vector(0,0,12000)); sky.light_component.set_editor_property('intensity',1.2)
    actor_sub.spawn_actor_from_class(u.SkyAtmosphere,u.Vector(0,0,0))
    # place the drivable Zafira explicitly at start so map is definitely not empty
    zcls=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira')
    if zcls:
        car=actor_sub.spawn_actor_from_class(zcls,u.Vector(sx,sy,sz+90),u.Rotator(0,yaw,0)); car.set_actor_label('Player_Zafira_Start')
    gm=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode')
    if gm: world.get_world_settings().set_editor_property('default_game_mode',gm)
    # mobile performance defaults on world
    world.get_world_settings().set_editor_property('kill_z',-8000)
    ok=u.EditorLoadingAndSavingUtils.save_map(world,MAP_PATH)
    report.update(success=bool(ok),length_km=meta['length_km'], start_yaw=yaw)
except Exception:
    report['success']=False; report['error']=traceback.format_exc(); u.log_error(report['error'])
(ROOT/'Scripts/long_track_build_report.json').write_text(json.dumps(report,indent=2,default=str))
print('LONG_TRACK_REPORT '+json.dumps(report,default=str))
assert report.get('success'), report