import unreal as u, pathlib, json, traceback
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
try:
    tools=u.AssetToolsHelpers.get_asset_tools()
    # Create bright unlit material helper for mobile visibility
    def unlit_mat(name,color):
        path=f'/Game/Zafira/LongTrack/Materials/M_{name}'
        m=u.EditorAssetLibrary.load_asset(path)
        if not m: m=tools.create_asset('M_'+name,'/Game/Zafira/LongTrack/Materials',u.Material,u.MaterialFactoryNew())
        m.modify()
        try: m.set_editor_property('shading_model', u.MaterialShadingModel.MSM_UNLIT)
        except Exception: pass
        c=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-420,0)
        c.constant=u.LinearColor(color[0],color[1],color[2],1)
        u.MaterialEditingLibrary.connect_material_property(c,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
        u.MaterialEditingLibrary.recompile_material(m); u.EditorAssetLibrary.save_asset(path); return m
    mats={
      'LT_Road':unlit_mat('LT_Road',(0.055,0.058,0.062)),
      'LT_Curbs_L':unlit_mat('LT_Curbs_L',(0.85,0.05,0.035)),
      'LT_Curbs_R':unlit_mat('LT_Curbs_R',(0.9,0.9,0.78)),
      'LT_Terrain':unlit_mat('LT_Terrain',(0.06,0.42,0.09)),
      'LT_Barriers':unlit_mat('LT_Barriers',(0.72,0.72,0.68)),
      'LT_CityBuildings':unlit_mat('LT_CityBuildings',(0.23,0.28,0.34)),
      'LT_Trees':unlit_mat('LT_Trees',(0.02,0.33,0.07)),
      'LT_StartGantry':unlit_mat('LT_StartGantry',(0.9,0.72,0.18)),
    }
    world=u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraLongTrack')
    actor_sub=u.get_editor_subsystem(u.EditorActorSubsystem)
    # Assign materials and remove mobile-problem sky/atmosphere/postprocess/fog duplicates
    removed=[]; assigned=[]
    for a in list(actor_sub.get_all_level_actors()):
        cls=a.get_class().get_name(); label=a.get_actor_label()
        if cls in ['SkyAtmosphere','ExponentialHeightFog','VolumetricCloud','PostProcessVolume'] or label.startswith('Zafira_Visual_PostProcess') or label.startswith('Zafira_Light_Atmosphere'):
            actor_sub.destroy_actor(a); removed.append(label); continue
        if cls=='DirectionalLight':
            a.light_component.set_editor_property('intensity',20.0); a.set_actor_rotation(u.Rotator(-45,45,0),False)
        if cls=='SkyLight':
            a.light_component.set_editor_property('intensity',6.0)
        if cls=='StaticMeshActor':
            smc=a.static_mesh_component; sm=smc.static_mesh
            if sm:
                nm=sm.get_name()
                if nm in mats: smc.set_material(0,mats[nm]); assigned.append(nm)
    # Add huge unlit blue sky dome/cube around map so mobile is not black even without SkyAtmosphere
    cube=u.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube')
    sky_mat=unlit_mat('LT_ClearBlueSky',(0.22,0.45,0.78))
    if cube:
        sky=actor_sub.spawn_actor_from_class(u.StaticMeshActor,u.Vector(0,0,-5000),u.Rotator(0,0,0)); sky.set_actor_label('Mobile_Clear_Blue_Backdrop'); sky.static_mesh_component.set_static_mesh(cube); sky.set_actor_scale3d(u.Vector(3000,3000,1)); sky.static_mesh_component.set_material(0,sky_mat)
    ok=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraLongTrack')
    report={'success':bool(ok),'removed':removed,'assigned_count':len(assigned),'assigned':sorted(set(assigned))}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(ROOT/'Scripts/fix_black_screen_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))
assert report.get('success'), report