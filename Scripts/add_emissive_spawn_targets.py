import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); tools=u.AssetToolsHelpers.get_asset_tools(); E=u.EditorAssetLibrary
report={}
def make_mat(name,color):
    path=f'/Game/Zafira/LongTrack/Materials/{name}'
    m=E.load_asset(path)
    if not m:
        m=tools.create_asset(name,'/Game/Zafira/LongTrack/Materials',u.Material,u.MaterialFactoryNew())
    m.modify()
    try: m.set_editor_property('shading_model', u.MaterialShadingModel.MSM_UNLIT)
    except Exception: pass
    c=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,0)
    c.constant=u.LinearColor(color[0],color[1],color[2],1)
    u.MaterialEditingLibrary.connect_material_property(c,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
    u.MaterialEditingLibrary.recompile_material(m); E.save_loaded_asset(m,False); return m
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraLongTrack')
    cube=E.load_asset('/Engine/BasicShapes/Cube.Cube')
    mats={
      'road':make_mat('M_FORCE_EMISSIVE_ROAD',(0.55,0.55,0.55)),
      'grass':make_mat('M_FORCE_EMISSIVE_GRASS',(0.0,0.8,0.12)),
      'red':make_mat('M_FORCE_EMISSIVE_RED',(2.0,0.0,0.0)),
      'yellow':make_mat('M_FORCE_EMISSIVE_YELLOW',(2.0,1.4,0.0)),
      'blue':make_mat('M_FORCE_EMISSIVE_BLUE',(0.1,0.45,2.0)),
      'white':make_mat('M_FORCE_EMISSIVE_WHITE',(2.0,2.0,2.0)),
    }
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label().startswith('CAMERA_TEST_'):
            u.EditorLevelLibrary.destroy_actor(a)
    # Put visible emissive objects exactly where the default pawn/player camera spawns and looks (+X)
    base=u.Vector(84724.34,-163.05,689.04)
    specs=[
      ('CAMERA_TEST_ROAD', u.Vector(base.x+2200,base.y,base.z-360), u.Vector(60,18,0.5),'road'),
      ('CAMERA_TEST_GRASS_L', u.Vector(base.x+2200,base.y-1700,base.z-370), u.Vector(60,8,0.5),'grass'),
      ('CAMERA_TEST_GRASS_R', u.Vector(base.x+2200,base.y+1700,base.z-370), u.Vector(60,8,0.5),'grass'),
      ('CAMERA_TEST_RED_LEFT', u.Vector(base.x+2500,base.y-650,base.z-100), u.Vector(20,1,5),'red'),
      ('CAMERA_TEST_YELLOW_RIGHT', u.Vector(base.x+2500,base.y+650,base.z-100), u.Vector(20,1,5),'yellow'),
      ('CAMERA_TEST_BLUE_BACKDROP', u.Vector(base.x+6000,base.y,base.z+1500), u.Vector(1,70,35),'blue'),
      ('CAMERA_TEST_WHITE_MARKER', u.Vector(base.x+1100,base.y,base.z-50), u.Vector(2,12,1),'white'),
    ]
    made=[]
    for name,loc,scale,key in specs:
        a=u.EditorLevelLibrary.spawn_actor_from_object(cube,loc,u.Rotator(0,0,0)); a.set_actor_label(name); a.set_actor_scale3d(scale)
        try: a.static_mesh_component.set_material(0,mats[key])
        except Exception: pass
        made.append(name)
    # Force playerstart to same known point/forward yaw and persist
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart':
            a.modify(); a.set_actor_location(base, False, False); a.set_actor_rotation(u.Rotator(0,0,0), False)
    ok_dirty=u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    ok_asset=E.save_asset('/Game/Zafira/Maps/ZafiraLongTrack',False)
    report={'success':True,'made':made,'save_dirty':ok_dirty,'save_asset':ok_asset}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'add_emissive_spawn_targets_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')