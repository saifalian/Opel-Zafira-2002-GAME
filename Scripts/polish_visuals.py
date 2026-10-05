import unreal as u, pathlib, json, traceback
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
MAT_DIR='/Game/Zafira/LongTrack/Materials'
MAP_PATH='/Game/Zafira/Maps/ZafiraLongTrack'
report={'materials':[], 'map':MAP_PATH}
# richer colors / roughness / emissive accents for visible, arcade-realistic look
SPECS={
 'LT_Road': {'color':(0.028,0.030,0.034),'rough':0.72,'metal':0.0},
 'LT_Curbs_L': {'color':(0.95,0.045,0.035),'rough':0.45},
 'LT_Curbs_R': {'color':(0.95,0.95,0.86),'rough':0.4},
 'LT_Terrain': {'color':(0.03,0.36,0.07),'rough':0.95},
 'LT_Barriers': {'color':(0.78,0.78,0.74),'rough':0.35,'metal':0.25},
 'LT_CityBuildings': {'color':(0.18,0.21,0.25),'rough':0.65,'metal':0.05},
 'LT_Trees': {'color':(0.02,0.28,0.055),'rough':0.9},
 'LT_StartGantry': {'color':(0.04,0.04,0.045),'rough':0.35,'metal':0.45},
}
def remake_material(name,spec):
    path=f'{MAT_DIR}/M_{name}'
    m=u.EditorAssetLibrary.load_asset(path)
    if not m: return False
    m.modify()
    # Clear old graph roughly by just adding new overriding nodes; output uses last connected pins.
    base=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,0)
    base.constant=u.LinearColor(*spec['color'],1)
    u.MaterialEditingLibrary.connect_material_property(base,'RGB',u.MaterialProperty.MP_BASE_COLOR)
    rough=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-500,220); rough.r=spec.get('rough',.75)
    u.MaterialEditingLibrary.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
    metal=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-500,420); metal.r=spec.get('metal',0.0)
    u.MaterialEditingLibrary.connect_material_property(metal,'',u.MaterialProperty.MP_METALLIC)
    if name in ['LT_Curbs_L','LT_Curbs_R']:
        em=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,620)
        c=spec['color']; em.constant=u.LinearColor(c[0]*0.18,c[1]*0.18,c[2]*0.18,1)
        u.MaterialEditingLibrary.connect_material_property(em,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
    u.MaterialEditingLibrary.recompile_material(m)
    u.EditorAssetLibrary.save_asset(path)
    return True
try:
    for k,v in SPECS.items():
        report['materials'].append({'name':k,'ok':remake_material(k,v)})
    world=u.EditorLoadingAndSavingUtils.load_map(MAP_PATH)
    actor_sub=u.get_editor_subsystem(u.EditorActorSubsystem)
    # improve existing lights and add fog/post-process for a bright daylight map
    for a in actor_sub.get_all_level_actors():
        cls=a.get_class().get_name(); label=a.get_actor_label()
        if cls=='DirectionalLight':
            a.light_component.set_editor_property('intensity',8.0)
            a.light_component.set_editor_property('light_color',u.Color(255,240,210,255))
            a.set_actor_rotation(u.Rotator(-38,38,0),False)
        elif cls=='SkyLight':
            a.light_component.set_editor_property('intensity',2.8)
            try: a.light_component.set_editor_property('lower_hemisphere_color',u.LinearColor(0.28,0.34,0.42,1))
            except Exception: pass
    # add/replace post-process volume
    pp=actor_sub.spawn_actor_from_class(u.PostProcessVolume,u.Vector(0,0,3000))
    pp.set_actor_label('Zafira_Visual_PostProcess')
    pp.set_editor_property('unbound', True)
    s=pp.get_editor_property('settings')
    for prop,val in [('override_auto_exposure_min_brightness',True),('override_auto_exposure_max_brightness',True),('auto_exposure_min_brightness',1.0),('auto_exposure_max_brightness',1.0),('override_auto_exposure_bias',True),('auto_exposure_bias',0.7),('override_bloom_intensity',True),('bloom_intensity',0.15),('override_color_grading_intensity',True),('color_grading_intensity',0.35)]:
        try: s.set_editor_property(prop,val)
        except Exception: pass
    pp.set_editor_property('settings',s)
    # fog for depth, low density to keep road visible
    fog=actor_sub.spawn_actor_from_class(u.ExponentialHeightFog,u.Vector(0,0,0))
    fog.set_actor_label('Zafira_Light_Atmosphere_Fog')
    try:
        fog.component.set_editor_property('fog_density',0.000012)
        fog.component.set_editor_property('fog_height_falloff',0.12)
        fog.component.set_editor_property('fog_inscattering_color',u.LinearColor(0.55,0.68,0.86,1))
    except Exception: pass
    # add colored start gate side signs so the map has a recognizable focal point
    start=u.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube')
    mat_blue=u.EditorAssetLibrary.load_asset(f'{MAT_DIR}/M_LT_CityBuildings')
    if start:
        meta=json.loads((ROOT/'SourceArt/LongTrack/long_track_meta.json').read_text()); sx,sy,sz=meta['start']; yaw=meta['start_yaw_deg']
        for j,(off,label) in enumerate([(-1500,'Blue_Start_Sign'),(1500,'Blue_Start_Sign_R')]):
            sign=actor_sub.spawn_actor_from_class(u.StaticMeshActor,u.Vector(sx,sy+off,sz+900),u.Rotator(0,yaw,0)); sign.set_actor_label(label); sign.static_mesh_component.set_static_mesh(start); sign.set_actor_scale3d(u.Vector(1.8,.12,.65))
            if mat_blue: sign.static_mesh_component.set_material(0,mat_blue)
    ok=u.EditorLoadingAndSavingUtils.save_map(world,MAP_PATH)
    report.update(success=bool(ok))
except Exception:
    report['success']=False; report['error']=traceback.format_exc(); u.log_error(report['error'])
(ROOT/'Scripts/polish_visuals_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))
assert report.get('success'), report