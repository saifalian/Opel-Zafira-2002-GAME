import unreal as u, pathlib, json, random, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
OUT='/Game/Zafira/Maps/ZafiraStraightSunny5KM'
r={}
try:
    world=u.EditorLoadingAndSavingUtils.new_map_from_template('/Engine/Maps/Templates/Template_Default', True)
    random.seed(7)
    cube=u.load_asset('/Engine/BasicShapes/Cube.Cube'); sphere=u.load_asset('/Engine/BasicShapes/Sphere.Sphere'); cyl=u.load_asset('/Engine/BasicShapes/Cylinder.Cylinder'); cone=u.load_asset('/Engine/BasicShapes/Cone.Cone')
    def mat(name,color):
        m=u.load_asset('/Game/Zafira/Straight5KM/'+name) or u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/Zafira/Straight5KM',u.Material,None)
        try:
            b=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-400,0); b.constant=color
            u.MaterialEditingLibrary.connect_material_property(b,'',u.MaterialProperty.MP_BASE_COLOR)
            rr=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-400,120); rr.r=.65
            u.MaterialEditingLibrary.connect_material_property(rr,'',u.MaterialProperty.MP_ROUGHNESS)
            u.MaterialEditingLibrary.recompile_material(m); u.EditorAssetLibrary.save_loaded_asset(m,False)
        except Exception: pass
        return m
    M={k:mat(k,c) for k,c in {
        'S_Road':u.LinearColor(.09,.095,.10,1),'S_Grass':u.LinearColor(.14,.32,.12,1),'S_Wall':u.LinearColor(.47,.47,.48,1),'S_Yellow':u.LinearColor(1,.68,.04,1),'S_White':u.LinearColor(.95,.95,.9,1),'S_Tree':u.LinearColor(.05,.50,.10,1),'S_Trunk':u.LinearColor(.33,.16,.06,1),'S_Red':u.LinearColor(.75,.12,.08,1),'S_Blue':u.LinearColor(.06,.22,.75,1),'S_Cream':u.LinearColor(.82,.68,.46,1),'S_Orange':u.LinearColor(1,.42,.04,1),'S_Purple':u.LinearColor(.45,.12,.72,1),'S_Rock':u.LinearColor(.32,.31,.30,1)}.items()}
    def spawn(mesh,label,loc,scale,mat,rot=(0,0,0),coll=True):
        a=u.EditorLevelLibrary.spawn_actor_from_object(mesh,u.Vector(*loc),u.Rotator(*rot)); a.set_actor_label(label); a.set_actor_scale3d(u.Vector(*scale))
        c=a.get_component_by_class(u.StaticMeshComponent)
        if c:
            c.set_material(0,mat); c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS if coll else u.CollisionEnabled.NO_COLLISION); c.set_collision_profile_name('BlockAll' if coll else 'NoCollision')
        return a
    length=500000; seg=25000; roadw=1800; floorw=7200
    # remove default floor/table-ish actors except lights/skies/cameras/playerstart
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        if a.get_class().get_name() in ['StaticMeshActor'] and not a.get_actor_label().startswith('S5N_'):
            try: u.EditorLevelLibrary.destroy_actor(a)
            except Exception: pass
    for i in range(20):
        x=i*seg+seg/2
        spawn(cube,f'S5N_Floor_{i}',(x,0,-20),(seg/100,floorw/100,.08),M['S_Grass'])
        spawn(cube,f'S5N_Road_{i}',(x,0,5),(seg/100,roadw/100,.08),M['S_Road'])
        spawn(cube,f'S5N_Barrier_L_{i}',(x,-roadw/2-160,85),(seg/100,.35,1.1),M['S_Yellow'])
        spawn(cube,f'S5N_Barrier_R_{i}',(x,roadw/2+160,85),(seg/100,.35,1.1),M['S_Yellow'])
        spawn(cube,f'S5N_Wall_L_{i}',(x,-floorw/2,180),(seg/100,.6,3.6),M['S_Wall'])
        spawn(cube,f'S5N_Wall_R_{i}',(x,floorw/2,180),(seg/100,.6,3.6),M['S_Wall'])
        for j in range(5): spawn(cube,f'S5N_Line_{i}_{j}',(i*seg+j*5000+1700,0,18),(18,.08,.025),M['S_White'],coll=False)
    spawn(cube,'S5N_StartEndWall',(length+900,0,180),(.6,floorw/100,3.6),M['S_Wall'])
    spawn(cube,'S5N_StartBackWall',(-1200,0,180),(.6,floorw/100,3.6),M['S_Wall'])
    # km signs as large colored boards + text both sides
    for km in range(1,6):
        x=km*100000
        for side,y in [('L',-1500),('R',1500)]:
            spawn(cube,f'S5N_{km}KM_Board_{side}',(x,y,260),(.25,5.0,2.0),M['S_Purple' if side=='L' else 'S_Blue'],rot=(0,0,0),coll=False)
            t=u.EditorLevelLibrary.spawn_actor_from_class(u.TextRenderActor,u.Vector(x,y,390),u.Rotator(0,90 if side=='L' else -90,0)); t.set_actor_label(f'S5N_{km}KM_PASS_TEXT_{side}')
            c=t.get_component_by_class(u.TextRenderComponent)
            if c: c.set_text(f'{km} KM PASS'); c.set_world_size(330); c.set_text_render_color(u.Color(255,245,40,255))
    count=0
    for km in range(5):
        base=km*100000
        for i in range(14):
            x=base+random.uniform(3000,97000); side=random.choice([-1,1]); y=side*random.uniform(2000,3300)
            spawn(cyl,f'S5N_TreeTrunk_{km}_{i}',(x,y,110),(.20,.20,2.2),M['S_Trunk']); spawn(sphere,f'S5N_TreeTop_{km}_{i}',(x,y,285),(1.5,1.5,1.2),M['S_Tree'],coll=False); count+=2
        for i in range(5):
            x=base+random.uniform(6000,94000); side=random.choice([-1,1]); y=side*random.uniform(3900,5400); h=random.uniform(4,10)
            spawn(cube,f'S5N_Building_{km}_{i}',(x,y,h*50),(random.uniform(5,10),random.uniform(4,8),h),random.choice([M['S_Red'],M['S_Blue'],M['S_Cream']])) ; count+=1
        for i in range(8):
            x=base+random.uniform(2500,96000); side=random.choice([-1,1]); y=side*random.uniform(1180,1450)
            spawn(cone,f'S5N_Cone_{km}_{i}',(x,y,45),(.45,.45,.9),M['S_Orange']); count+=1
    # sunny clear top sun / bright sky
    for a in u.EditorLevelLibrary.get_all_level_actors():
        cls=a.get_class().get_name()
        if 'DirectionalLight' in cls:
            a.set_actor_rotation(u.Rotator(-88,20,0),False); comp=a.get_component_by_class(u.DirectionalLightComponent)
            if comp: comp.set_intensity(10.0); comp.set_light_color(u.LinearColor(1,.95,.82,1),True)
        if 'SkyLight' in cls:
            comp=a.get_component_by_class(u.SkyLightComponent)
            if comp: comp.set_intensity(1.6)
    ps=u.EditorLevelLibrary.spawn_actor_from_class(u.PlayerStart,u.Vector(700,0,140),u.Rotator(0,0,0)); ps.set_actor_label('S5N_PlayerStart')
    cam=u.EditorLevelLibrary.spawn_actor_from_class(u.CameraActor,u.Vector(-1000,0,620),u.Rotator(-12,0,0)); cam.set_actor_label('S5N_ViewCamera'); cam.get_component_by_class(u.CameraComponent).set_field_of_view(82)
    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(),OUT)
    r={'success':bool(ok),'map':OUT,'length_km':5,'road':'straight','scenery_added':count,'weather':'sunny clear top sun'}
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
S.joinpath('straight_sunny_newmap_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
