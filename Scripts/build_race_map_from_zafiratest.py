import unreal as u, pathlib, json, traceback, math
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; tools=u.AssetToolsHelpers.get_asset_tools()
report={}
def mat(name,color,em=0.08):
    m=E.load_asset(f'/Game/Zafira/LongTrack/Materials/{name}') or tools.create_asset(name,'/Game/Zafira/LongTrack/Materials',u.Material,u.MaterialFactoryNew())
    m.modify();
    try: m.set_editor_property('two_sided', True)
    except Exception: pass
    b=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,0); b.constant=u.LinearColor(*color,1); u.MaterialEditingLibrary.connect_material_property(b,'RGB',u.MaterialProperty.MP_BASE_COLOR)
    e=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,230); e.constant=u.LinearColor(color[0]*em,color[1]*em,color[2]*em,1); u.MaterialEditingLibrary.connect_material_property(e,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
    r=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-500,430); r.r=0.8; u.MaterialEditingLibrary.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
    u.MaterialEditingLibrary.recompile_material(m); E.save_loaded_asset(m,False); return m

def spawn(mesh,label,loc,scale,material,rot=None):
    a=u.EditorLevelLibrary.spawn_actor_from_object(mesh,loc,rot or u.Rotator(0,0,0)); a.set_actor_label(label); a.set_actor_scale3d(scale)
    try: a.static_mesh_component.set_material(0,material)
    except Exception: pass
    return a
try:
    # Use original ZafiraTest as base because its real vehicle/control/audio path is known visible and moving.
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraTest')
    world=u.EditorLevelLibrary.get_editor_world()
    cube=E.load_asset('/Engine/BasicShapes/Cube.Cube'); cyl=E.load_asset('/Engine/BasicShapes/Cylinder.Cylinder'); cone=E.load_asset('/Engine/BasicShapes/Cone.Cone')
    mats={
      'road':mat('M_RACE_ASPHALT_CLEAN',(0.09,0.095,0.10),0.12), 'grass':mat('M_RACE_GRASS_CLEAN',(0.035,0.45,0.075),0.10),
      'line':mat('M_RACE_YELLOW_LINE',(1.0,0.78,0.12),0.2), 'curbR':mat('M_RACE_CURB_RED',(0.95,0.02,0.015),0.15), 'curbW':mat('M_RACE_CURB_WHITE',(0.9,0.9,0.82),0.08),
      'barrier':mat('M_RACE_BARRIER',(0.92,0.68,0.10),0.12), 'trunk':mat('M_RACE_TRUNK',(0.28,0.12,0.04),0.05), 'leaf':mat('M_RACE_LEAF',(0.02,0.34,0.06),0.1),
      'buildingA':mat('M_RACE_BUILDING_A',(0.28,0.36,0.52),0.08), 'buildingB':mat('M_RACE_BUILDING_B',(0.50,0.36,0.24),0.06), 'glass':mat('M_RACE_GLASS',(0.35,0.58,0.8),0.15)}
    # Clean old generated actors from this base if re-run.
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        lab=a.get_actor_label()
        if lab.startswith('RACE_'):
            u.EditorLevelLibrary.destroy_actor(a)
    # Wide continuous-looking course on the original ground plane: 5.4 km, curves and elevation via visual slabs.
    pts=[]; length=0; prev=None
    for i in range(70):
        x=i*7800.0
        y=math.sin(i*0.18)*2600 + math.sin(i*0.42)*650
        z=80 + math.sin(i*0.14)*80
        if prev: length+=math.dist((x,y,z),prev)
        prev=(x,y,z); pts.append((x,y,z))
    road_w=900
    for i,(x,y,z) in enumerate(pts):
        if i<len(pts)-1: nx,ny,nz=pts[i+1]; yaw=math.degrees(math.atan2(ny-y,nx-x))
        else: px,py,pz=pts[i-1]; yaw=math.degrees(math.atan2(y-py,x-px))
        rot=u.Rotator(0,yaw,0)
        spawn(cube,f'RACE_Road_{i:02d}',u.Vector(x,y,z),u.Vector(85,road_w/200,0.12),mats['road'],rot)
        spawn(cube,f'RACE_Centre_{i:02d}',u.Vector(x,y,z+18),u.Vector(16,0.055,0.04),mats['line'],rot)
        for side in [-1,1]:
            spawn(cube,f'RACE_Curb_{i:02d}_{side}',u.Vector(x,y+side*road_w/2,z+24),u.Vector(85,0.22,0.18),mats['curbR' if (i+side)%2 else 'curbW'],rot)
            spawn(cube,f'RACE_Shoulder_{i:02d}_{side}',u.Vector(x,y+side*(road_w/2+330),z-12),u.Vector(85,3.2,0.08),mats['grass'],rot)
            if i%2==0:
                spawn(cube,f'RACE_Barrier_{i:02d}_{side}',u.Vector(x,y+side*(road_w/2+130),z+82),u.Vector(78,0.12,0.55),mats['barrier'],rot)
        if i%3==0 and i>1:
            for side in [-1,1]:
                tx=x+800; ty=y+side*(road_w/2+800); tz=z+80
                spawn(cyl,f'RACE_Tree_Trunk_{i}_{side}',u.Vector(tx,ty,tz),u.Vector(0.35,0.35,1.8),mats['trunk'])
                spawn(cone,f'RACE_Tree_Leaf_{i}_{side}',u.Vector(tx,ty,tz+205),u.Vector(1.4,1.4,1.9),mats['leaf'])
        if i%6==0 and i>4:
            for side in [1,-1]:
                bmat=mats['buildingA'] if side>0 else mats['buildingB']
                spawn(cube,f'RACE_City_{i}_{side}',u.Vector(x,y+side*(road_w/2+1500),z+330),u.Vector(3.5,3.5,5.5),bmat,u.Rotator(0,yaw+side*5,0))
                spawn(cube,f'RACE_Glass_{i}_{side}',u.Vector(x-85,y+side*(road_w/2+1492),z+350),u.Vector(0.08,3.0,3.3),mats['glass'],u.Rotator(0,yaw+side*5,0))
    # place real vehicle start on original working base, facing road start
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart':
            a.set_actor_location(u.Vector(-650,0,360),False,False); a.set_actor_rotation(u.Rotator(0,0,0),False)
    ws=world.get_world_settings(); ws.modify(); gm=E.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode');
    if gm: ws.set_editor_property('default_game_mode', gm)
    ok=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraRaceMap')
    report={'success':True,'save_map':ok,'map':'/Game/Zafira/Maps/ZafiraRaceMap','approx_length_m':round(length/100,1),'base':'ZafiraTest real vehicle/control base'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'build_race_map_from_zafiratest_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')