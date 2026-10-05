import unreal as u, pathlib, json, traceback, math
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
MAP='/Game/Zafira/Maps/ZafiraLongTrack'
report={}
try:
    tools=u.AssetToolsHelpers.get_asset_tools()
    def mat(name,color):
        path=f'/Game/Zafira/LongTrack/Materials/M_{name}'
        m=u.EditorAssetLibrary.load_asset(path) or tools.create_asset('M_'+name,'/Game/Zafira/LongTrack/Materials',u.Material,u.MaterialFactoryNew())
        m.modify()
        try: m.set_editor_property('shading_model', u.MaterialShadingModel.MSM_UNLIT)
        except Exception: pass
        c=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,0)
        c.constant=u.LinearColor(color[0],color[1],color[2],1)
        u.MaterialEditingLibrary.connect_material_property(c,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
        u.MaterialEditingLibrary.recompile_material(m); u.EditorAssetLibrary.save_asset(path); return m
    asphalt=mat('MOBILE_VISIBLE_ASPHALT',(0.20,0.21,0.22)); grass=mat('MOBILE_VISIBLE_GRASS',(0.05,0.50,0.08)); red=mat('MOBILE_VISIBLE_RED',(0.95,0.05,0.03)); white=mat('MOBILE_VISIBLE_WHITE',(0.95,0.95,0.82)); blue=mat('MOBILE_VISIBLE_BLUE',(0.12,0.38,0.95)); yellow=mat('MOBILE_VISIBLE_YELLOW',(1.0,0.75,0.08)); tree=mat('MOBILE_VISIBLE_TREE',(0.03,0.32,0.06)); city=mat('MOBILE_VISIBLE_CITY',(0.25,0.32,0.40))
    world=u.EditorLoadingAndSavingUtils.load_map(MAP)
    actor_sub=u.get_editor_subsystem(u.EditorActorSubsystem)
    cube=u.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube')
    meta=json.loads((ROOT/'SourceArt/LongTrack/long_track_meta.json').read_text()); pts=meta['points']; sx,sy,sz=meta['start']; yaw=meta['start_yaw_deg']
    # remove prior visual fallback actors to avoid clutter
    for a in list(actor_sub.get_all_level_actors()):
        if a.get_actor_label().startswith('MOBILE_') or a.get_actor_label().startswith('Mobile_Clear'):
            actor_sub.destroy_actor(a)
    def box(label,loc,scale,material,rot_yaw=0):
        a=actor_sub.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*loc),u.Rotator(0,rot_yaw,0)); a.set_actor_label(label); a.static_mesh_component.set_static_mesh(cube); a.set_actor_scale3d(u.Vector(*scale)); a.static_mesh_component.set_material(0,material); return a
    # big guaranteed-visible start platform and road under the player/camera
    box('MOBILE_Start_Asphalt_Visible',(sx,sy,sz-65),(80,18,0.35),asphalt,yaw)
    box('MOBILE_Start_Grass_Left',(sx-2500,sy,sz-90),(25,22,0.25),grass,yaw)
    box('MOBILE_Start_Grass_Right',(sx+2500,sy,sz-90),(25,22,0.25),grass,yaw)
    box('MOBILE_Start_Line',(sx,sy,sz+8),(0.18,12,0.08),white,yaw)
    # bright lane/curb markers along first 1.2km sampled from generated course
    for idx,i in enumerate(range(0,min(170,len(pts)),5)):
        p=pts[i]; q=pts[(i+1)%len(pts)]; ang=math.degrees(math.atan2(q[1]-p[1], q[0]-p[0]))
        box('MOBILE_RoadSeg_%03d'%idx,(p[0],p[1],p[2]-52),(8.0,9.0,0.18),asphalt,ang)
        box('MOBILE_CurbRed_%03d'%idx,(p[0]-520,p[1],p[2]-42),(0.55,1.6,0.12),red,ang)
        box('MOBILE_CurbWhite_%03d'%idx,(p[0]+520,p[1],p[2]-42),(0.55,1.6,0.12),white,ang)
        if idx%4==0:
            box('MOBILE_Barrier_%03d_L'%idx,(p[0]-820,p[1],p[2]+55),(0.35,2.2,0.7),yellow,ang)
            box('MOBILE_Barrier_%03d_R'%idx,(p[0]+820,p[1],p[2]+55),(0.35,2.2,0.7),yellow,ang)
    # simple visible trees/buildings close enough to see
    for k,i in enumerate(range(20,150,10)):
        p=pts[i]
        box('MOBILE_Tree_%02d'%k,(p[0]-2600,p[1]+1200,p[2]+260),(1.2,1.2,5.0),tree,0)
        if k%2==0: box('MOBILE_Building_%02d'%k,(p[0]+3600,p[1]-900,p[2]+650),(3.2,3.2,9.0),city,0)
    # make lighting trivial and bright
    for a in actor_sub.get_all_level_actors():
        cls=a.get_class().get_name()
        if cls=='DirectionalLight': a.light_component.set_editor_property('intensity',30.0); a.set_actor_rotation(u.Rotator(-50,35,0),False)
        if cls=='SkyLight': a.light_component.set_editor_property('intensity',8.0)
    ok=u.EditorLoadingAndSavingUtils.save_map(world,MAP)
    report={'success':bool(ok),'actors_added':'visible mobile fallback road/curbs/barriers/trees/buildings','map':MAP}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(ROOT/'Scripts/mobile_visibility_fix_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))
assert report.get('success'), report