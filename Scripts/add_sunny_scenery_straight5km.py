import unreal as u, pathlib, json, random, traceback, math
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
MAP='/Game/Zafira/Maps/ZafiraStraight5KM'
report={}
try:
    u.EditorLoadingAndSavingUtils.load_map(MAP)
    cube=u.load_asset('/Engine/BasicShapes/Cube.Cube')
    sphere=u.load_asset('/Engine/BasicShapes/Sphere.Sphere')
    cone=u.load_asset('/Engine/BasicShapes/Cone.Cone')
    cyl=u.load_asset('/Engine/BasicShapes/Cylinder.Cylinder')
    random.seed(42)
    def mat(name, color, rough=0.65):
        path='/Game/Zafira/Straight5KM/'+name
        m=u.load_asset(path)
        if not m:
            m=u.AssetToolsHelpers.get_asset_tools().create_asset(name,'/Game/Zafira/Straight5KM',u.Material,None)
        try:
            m.set_editor_property('shading_model',u.MaterialShadingModel.MSM_DEFAULT_LIT)
            base=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-400,0); base.constant=color
            u.MaterialEditingLibrary.connect_material_property(base,'',u.MaterialProperty.MP_BASE_COLOR)
            r=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-400,120); r.r=rough
            u.MaterialEditingLibrary.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
            u.MaterialEditingLibrary.recompile_material(m); u.EditorAssetLibrary.save_loaded_asset(m,False)
        except Exception: pass
        return m
    mats={
      'leaf1':mat('M_S5_LeafBright',u.LinearColor(0.05,0.42,0.08,1)),
      'leaf2':mat('M_S5_LeafOlive',u.LinearColor(0.18,0.48,0.10,1)),
      'leaf3':mat('M_S5_LeafSpring',u.LinearColor(0.10,0.60,0.18,1)),
      'trunk':mat('M_S5_Trunk',u.LinearColor(0.33,0.17,0.07,1)),
      'red':mat('M_S5_BuildingRed',u.LinearColor(0.70,0.12,0.08,1)),
      'blue':mat('M_S5_BuildingBlue',u.LinearColor(0.08,0.22,0.68,1)),
      'cream':mat('M_S5_BuildingCream',u.LinearColor(0.82,0.68,0.45,1)),
      'glass':mat('M_S5_GlassCyan',u.LinearColor(0.18,0.70,0.92,1)),
      'orange':mat('M_S5_OrangeStuff',u.LinearColor(1.0,0.40,0.04,1)),
      'purple':mat('M_S5_PurpleStuff',u.LinearColor(0.48,0.16,0.75,1)),
      'rock':mat('M_S5_Rock',u.LinearColor(0.33,0.32,0.30,1)),
      'white':mat('M_S5_White',u.LinearColor(0.9,0.9,0.86,1)),
      'sun':mat('M_S5_SunYellow',u.LinearColor(1.0,0.86,0.14,1),0.35),
    }
    def spawn(mesh,label,loc,scale,material,rot=(0,0,0),collision=True):
        a=u.EditorLevelLibrary.spawn_actor_from_object(mesh,u.Vector(*loc),u.Rotator(*rot)); a.set_actor_label(label); a.set_actor_scale3d(u.Vector(*scale))
        c=a.get_component_by_class(u.StaticMeshComponent)
        if c:
            c.set_material(0,material)
            c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS if collision else u.CollisionEnabled.NO_COLLISION)
            c.set_collision_profile_name('BlockAll' if collision else 'NoCollision')
        return a
    # remove old scenery only
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label().startswith('S5_SC_'):
            u.EditorLevelLibrary.destroy_actor(a)
    count=0
    # colorful realistic-ish roadside: trees, shrubs, buildings, signs, rocks, light poles, cones
    for km in range(5):
        base=km*100000
        for i in range(18):
            x=base+random.uniform(2500,95000)
            side=random.choice([-1,1])
            y=side*random.uniform(1700,3100)
            # tree trunk and crown
            h=random.uniform(180,360)
            spawn(cyl,f'S5_SC_TreeTrunk_{km}_{i}',(x,y,h/2),(0.22,0.22,h/100),mats['trunk']); count+=1
            spawn(sphere,f'S5_SC_TreeTop_{km}_{i}',(x,y,h+100),(random.uniform(1.4,2.6),random.uniform(1.4,2.6),random.uniform(1.0,1.8)),random.choice([mats['leaf1'],mats['leaf2'],mats['leaf3']]),collision=False); count+=1
        for i in range(8):
            x=base+random.uniform(5000,95000); side=random.choice([-1,1]); y=side*random.uniform(3800,5200)
            w=random.uniform(5,12); d=random.uniform(4,8); h=random.uniform(3,11)
            spawn(cube,f'S5_SC_Building_{km}_{i}',(x,y,h*50),(w,d,h),random.choice([mats['red'],mats['blue'],mats['cream'],mats['glass']])); count+=1
            # colored roof
            spawn(cube,f'S5_SC_Roof_{km}_{i}',(x,y,h*100+25),(w*1.06,d*1.06,0.25),random.choice([mats['orange'],mats['purple'],mats['rock']])); count+=1
        for i in range(10):
            x=base+random.uniform(2000,98000); side=random.choice([-1,1]); y=side*random.uniform(1250,1550)
            spawn(cone,f'S5_SC_Cone_{km}_{i}',(x,y,45),(0.45,0.45,0.9),mats['orange']); count+=1
        for i in range(6):
            x=base+random.uniform(8000,92000); side=random.choice([-1,1]); y=side*random.uniform(2600,3300)
            spawn(sphere,f'S5_SC_Rock_{km}_{i}',(x,y,35),(random.uniform(0.7,1.5),random.uniform(0.7,1.5),random.uniform(0.35,0.8)),mats['rock']); count+=1
        for i in range(5):
            x=base+10000+i*18000; side=random.choice([-1,1]); y=side*1250
            spawn(cyl,f'S5_SC_LightPole_{km}_{i}',(x,y,320),(0.09,0.09,6.4),mats['white']); count+=1
            spawn(sphere,f'S5_SC_LightBall_{km}_{i}',(x,y,660),(0.35,0.35,0.35),mats['sun'],collision=False); count+=1
    # sunny clear weather: high top sun, blue sky, bright lighting, no fog/rain
    for a in u.EditorLevelLibrary.get_all_level_actors():
        cls=a.get_class().get_name(); lab=a.get_actor_label().lower()
        if 'DirectionalLight' in cls or 'sun' in lab:
            a.set_actor_label('S5_Clear_Top_Sun')
            a.set_actor_rotation(u.Rotator(-88,35,0),False)
            try:
                comp=a.get_component_by_class(u.DirectionalLightComponent)
                comp.set_intensity(8.0); comp.set_light_color(u.LinearColor(1.0,0.94,0.82,1), True)
                comp.set_editor_property('mobility',u.ComponentMobility.MOVABLE)
            except Exception: pass
        if 'SkyLight' in cls:
            try:
                comp=a.get_component_by_class(u.SkyLightComponent); comp.set_intensity(1.4); comp.set_editor_property('mobility',u.ComponentMobility.MOVABLE)
            except Exception: pass
        if 'ExponentialHeightFog' in cls:
            try: a.get_component_by_class(u.ExponentialHeightFogComponent).set_fog_density(0.0005)
            except Exception: pass
    # add a decorative visible sun disc high ahead (non-colliding)
    spawn(sphere,'S5_SC_Top_Sun_Visual',(150000,0,8500),(18,18,18),mats['sun'],collision=False)
    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(), MAP)
    report={'success':bool(ok),'map':MAP,'scenery_actors_added':count+1,'weather':'sunny clear, top sun, bright skylight','features':['trees','buildings','cones','rocks','light poles','colorful roofs','sun disc']}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'sunny_scenery_straight5km_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
