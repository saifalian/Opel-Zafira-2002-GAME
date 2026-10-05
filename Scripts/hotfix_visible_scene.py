import unreal as u, pathlib, json, traceback, math
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
MAP='/Game/Zafira/Maps/ZafiraLongTrack'
r={}
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
    road=mat('HOTFIX_VISIBLE_ROAD',(1.4,1.45,1.5)); grass=mat('HOTFIX_VISIBLE_GRASS',(0.10,1.2,0.14)); blue=mat('HOTFIX_VISIBLE_BLUE_SKY',(0.18,0.50,1.8)); red=mat('HOTFIX_VISIBLE_RED',(2.0,0.05,0.02)); yellow=mat('HOTFIX_VISIBLE_YELLOW',(2.0,1.45,0.05)); white=mat('HOTFIX_VISIBLE_WHITE',(2.0,2.0,1.75));
    world=u.EditorLoadingAndSavingUtils.load_map(MAP)
    actor_sub=u.get_editor_subsystem(u.EditorActorSubsystem); cube=u.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube')
    meta=json.loads((ROOT/'SourceArt/LongTrack/long_track_meta.json').read_text()); sx,sy,sz=meta['start']; yaw=meta['start_yaw_deg']; rad=math.radians(yaw); fx,fy=math.cos(rad),math.sin(rad); rx,ry=-fy,fx
    # remove old hotfix visible actors
    for a in list(actor_sub.get_all_level_actors()):
        if a.get_actor_label().startswith('HOTFIX_'):
            actor_sub.destroy_actor(a)
    def loc(f=0,rgt=0,z=0): return (sx+fx*f+rx*rgt, sy+fy*f+ry*rgt, sz+z)
    def box(label, f,rgt,z, scale, material, rot_yaw=None):
        a=actor_sub.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*loc(f,rgt,z)),u.Rotator(0, yaw if rot_yaw is None else rot_yaw, 0)); a.set_actor_label(label); a.static_mesh_component.set_static_mesh(cube); a.set_actor_scale3d(u.Vector(*scale)); a.static_mesh_component.set_material(0,material); return a
    # Very bright visible world immediately around/under car and in camera view
    box('HOTFIX_Road_UnderCar', 0,0,-150, (120,18,0.30), road)
    box('HOTFIX_Road_Ahead_1', 7000,0,-145, (140,18,0.30), road)
    box('HOTFIX_Left_Grass', 4500,-2300,-170, (160,28,0.25), grass)
    box('HOTFIX_Right_Grass', 4500,2300,-170, (160,28,0.25), grass)
    for i,f in enumerate(range(0,24000,2500)):
        box(f'HOTFIX_Left_Curb_{i}', f,-620,-100, (2.0,1.8,0.18), red)
        box(f'HOTFIX_Right_Curb_{i}', f,620,-100, (2.0,1.8,0.18), white)
        box(f'HOTFIX_Left_Barrier_{i}', f,-1050,80, (1.2,4.0,1.0), yellow)
        box(f'HOTFIX_Right_Barrier_{i}', f,1050,80, (1.2,4.0,1.0), yellow)
    # huge blue background above horizon, placed in front of camera direction and high
    box('HOTFIX_Blue_Sky_Backdrop', 30000,0,9000, (500,4,120), blue)
    box('HOTFIX_Blue_Sky_Ceiling', 10000,0,15000, (500,500,2), blue)
    # move PlayerStart slightly forward and high so it doesn't collide but sees road
    for a in actor_sub.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart':
            x,y,z=loc(1500,0,850); a.set_actor_location(u.Vector(x,y,z),False,False); a.set_actor_rotation(u.Rotator(0,yaw,0),False)
    ok=u.EditorLoadingAndSavingUtils.save_map(world,MAP)
    r={'success':bool(ok),'note':'added ultra-bright immediate PC/mobile visible road, grass, curbs, barriers, blue backdrop; moved PlayerStart forward/up'}
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
(ROOT/'Scripts/hotfix_visible_scene_report.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,default=str))
assert r.get('success'), r