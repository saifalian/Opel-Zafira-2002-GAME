import unreal as u, pathlib, json, traceback, math
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
E=u.EditorAssetLibrary; tools=u.AssetToolsHelpers.get_asset_tools()
report={}

def mat(name, color, rough=0.85):
    path=f'/Game/Zafira/LongTrack/Materials/{name}'
    m=E.load_asset(path) or tools.create_asset(name,'/Game/Zafira/LongTrack/Materials',u.Material,u.MaterialFactoryNew())
    m.modify()
    try: m.set_editor_property('two_sided', True)
    except Exception: pass
    base=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,0)
    base.constant=u.LinearColor(color[0],color[1],color[2],1)
    u.MaterialEditingLibrary.connect_material_property(base,'RGB',u.MaterialProperty.MP_BASE_COLOR)
    emis=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,220)
    # faint emissive keeps it readable on PC/mobile without making it neon
    emis.constant=u.LinearColor(color[0]*0.18,color[1]*0.18,color[2]*0.18,1)
    u.MaterialEditingLibrary.connect_material_property(emis,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
    r=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-500,430); r.r=rough
    u.MaterialEditingLibrary.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
    u.MaterialEditingLibrary.recompile_material(m); E.save_loaded_asset(m,False); return m

def spawn(mesh,label,loc,scale,material,rot=None):
    a=u.EditorLevelLibrary.spawn_actor_from_object(mesh,loc,rot or u.Rotator(0,0,0))
    a.set_actor_label(label); a.set_actor_scale3d(scale)
    try: a.static_mesh_component.set_material(0,material)
    except Exception: pass
    return a

try:
    # rebuild from verified-visible engine template so no black screen
    world=u.EditorLoadingAndSavingUtils.new_map_from_template('/Engine/Maps/Templates/Template_Default', True)
    cube=E.load_asset('/Engine/BasicShapes/Cube.Cube')
    cyl=E.load_asset('/Engine/BasicShapes/Cylinder.Cylinder')
    cone=E.load_asset('/Engine/BasicShapes/Cone.Cone')
    sphere=E.load_asset('/Engine/BasicShapes/Sphere.Sphere')
    mats={
      'asphalt':mat('M_BEAUTIFUL_ASPHALT',(0.12,0.125,0.13)),
      'grass':mat('M_BEAUTIFUL_GRASS',(0.035,0.34,0.065)),
      'curb_red':mat('M_BEAUTIFUL_CURB_RED',(0.9,0.025,0.018)),
      'curb_white':mat('M_BEAUTIFUL_CURB_WHITE',(1.0,0.94,0.82)),
      'line':mat('M_BEAUTIFUL_ROAD_LINE',(1.0,0.85,0.18)),
      'barrier':mat('M_BEAUTIFUL_BARRIER',(0.95,0.72,0.12)),
      'trunk':mat('M_BEAUTIFUL_TREE_TRUNK',(0.26,0.11,0.035)),
      'leaf':mat('M_BEAUTIFUL_TREE_LEAF',(0.02,0.42,0.08)),
      'building1':mat('M_BEAUTIFUL_BUILDING_BLUE',(0.16,0.24,0.42)),
      'building2':mat('M_BEAUTIFUL_BUILDING_WARM',(0.48,0.36,0.25)),
      'glass':mat('M_BEAUTIFUL_GLASS',(0.28,0.48,0.75)),
      'gantry':mat('M_BEAUTIFUL_GANTRY',(0.06,0.06,0.07)),
    }
    # Parametric 5.4km-ish road: 72 x 75m segments, visible sweeping curves and hills
    points=[]
    length=0.0
    prev=None
    for i in range(72):
        x=i*7500.0
        y=math.sin(i*0.25)*1300 + math.sin(i*0.08)*600
        z=70 + math.sin(i*0.18)*120 + max(0, math.sin((i-18)*0.10))*90
        if prev: length += math.dist((x,y,z), prev)
        prev=(x,y,z); points.append((x,y,z))
    road_w=720; grass_w=900
    for i,(x,y,z) in enumerate(points):
        yaw=0
        if i < len(points)-1:
            nx,ny,nz=points[i+1]; yaw=math.degrees(math.atan2(ny-y,nx-x))
        elif i>0:
            px,py,pz=points[i-1]; yaw=math.degrees(math.atan2(y-py,x-px))
        rot=u.Rotator(0,yaw,0)
        spawn(cube,f'BT_Road_{i:02d}',u.Vector(x,y,z),u.Vector(80.0,road_w/200,0.16),mats['asphalt'],rot)
        spawn(cube,f'BT_Grass_L_{i:02d}',u.Vector(x,y-road_w/2-grass_w/2,z-18),u.Vector(80.0,grass_w/200,0.12),mats['grass'],rot)
        spawn(cube,f'BT_Grass_R_{i:02d}',u.Vector(x,y+road_w/2+grass_w/2,z-18),u.Vector(80.0,grass_w/200,0.12),mats['grass'],rot)
        spawn(cube,f'BT_CentreLine_{i:02d}',u.Vector(x,y,z+24),u.Vector(18.0,0.08,0.035),mats['line'],rot)
        spawn(cube,f'BT_Curb_L_{i:02d}',u.Vector(x,y-road_w/2,z+35),u.Vector(80.0,0.20,0.20),mats['curb_red' if i%2==0 else 'curb_white'],rot)
        spawn(cube,f'BT_Curb_R_{i:02d}',u.Vector(x,y+road_w/2,z+35),u.Vector(80.0,0.20,0.20),mats['curb_white' if i%2==0 else 'curb_red'],rot)
        if i%2==0:
            spawn(cube,f'BT_Barrier_L_{i:02d}',u.Vector(x,y-road_w/2-105,z+105),u.Vector(75.0,0.13,0.75),mats['barrier'],rot)
            spawn(cube,f'BT_Barrier_R_{i:02d}',u.Vector(x,y+road_w/2+105,z+105),u.Vector(75.0,0.13,0.75),mats['barrier'],rot)
        if i%3==0 and i>2:
            # trees alternating sides
            for side in [-1,1]:
                tx=x; ty=y+side*(road_w/2+520+(i%5)*70); tz=z+95
                spawn(cyl,f'BT_TreeTrunk_{i:02d}_{side}',u.Vector(tx,ty,tz),u.Vector(0.28,0.28,2.1),mats['trunk'])
                spawn(cone,f'BT_TreeLeaf_{i:02d}_{side}',u.Vector(tx,ty,tz+220),u.Vector(1.35,1.35,2.1),mats['leaf'])
        if i%5==0 and i>8:
            # roadside city blocks, offset and colored so they don't read as black walls
            for side in [-1,1]:
                h=3.5+(i%6)*0.85
                bmat=mats['building1'] if (i+side)%2==0 else mats['building2']
                b=spawn(cube,f'BT_City_{i:02d}_{side}',u.Vector(x,y+side*(road_w/2+1250),z+180*h/2),u.Vector(2.8,3.0,h),bmat,u.Rotator(0,yaw+8*side,0))
                spawn(cube,f'BT_CityGlass_{i:02d}_{side}',u.Vector(x-70,y+side*(road_w/2+1242),z+180*h/2+20),u.Vector(0.08,2.7,h*0.55),mats['glass'],u.Rotator(0,yaw+8*side,0))
    # start gantry
    x,y,z=points[0]
    spawn(cube,'BT_Start_Gantry_L',u.Vector(x+260,y-road_w/2-180,z+360),u.Vector(0.35,0.35,4.0),mats['gantry'])
    spawn(cube,'BT_Start_Gantry_R',u.Vector(x+260,y+road_w/2+180,z+360),u.Vector(0.35,0.35,4.0),mats['gantry'])
    spawn(cube,'BT_Start_Gantry_Top',u.Vector(x+260,y,z+720),u.Vector(0.35,5.5,0.35),mats['gantry'])
    # player start just behind first segment, car facing down road
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart':
            a.set_actor_location(u.Vector(x-650,y,z+430),False,False); a.set_actor_rotation(u.Rotator(0,0,0),False)
    # keep real Zafira game mode
    ws=world.get_world_settings(); ws.modify()
    gm=E.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode') or E.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode')
    ws.set_editor_property('default_game_mode', gm)
    ok=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraPlayableTrack')
    report={'success':True,'save_map':ok,'segments':len(points),'approx_length_m':round(length/100,1),'map':'/Game/Zafira/Maps/ZafiraPlayableTrack','note':'Rebuilt visible template-based track with long curves, elevation, trees, city blocks, barriers, curbs.'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'rebuild_beautiful_playable_track_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')
