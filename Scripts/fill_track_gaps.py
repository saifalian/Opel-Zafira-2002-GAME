import unreal as u, pathlib, json, traceback, math
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; tools=u.AssetToolsHelpers.get_asset_tools()
report={}
def mat(name,color):
    m=E.load_asset(f'/Game/Zafira/LongTrack/Materials/{name}') or tools.create_asset(name,'/Game/Zafira/LongTrack/Materials',u.Material,u.MaterialFactoryNew())
    m.modify()
    b=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,0); b.constant=u.LinearColor(*color,1); u.MaterialEditingLibrary.connect_material_property(b,'RGB',u.MaterialProperty.MP_BASE_COLOR)
    e=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,220); e.constant=u.LinearColor(color[0]*.25,color[1]*.25,color[2]*.25,1); u.MaterialEditingLibrary.connect_material_property(e,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
    u.MaterialEditingLibrary.recompile_material(m); E.save_loaded_asset(m,False); return m
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraPlayableTrack')
    cube=E.load_asset('/Engine/BasicShapes/Cube.Cube')
    grass=mat('M_TRACK_GREEN_BRIGHT',(0.05,0.65,0.10)); asphalt=mat('M_BEAUTIFUL_ASPHALT',(0.18,0.18,0.18)); shoulder=mat('M_TRACK_SHOULDER_GREY',(0.20,0.20,0.18))
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label().startswith('Fill_'):
            u.EditorLevelLibrary.destroy_actor(a)
    for i in range(18):
        x=i*7500.0; y=math.sin(i*0.25)*1300 + math.sin(i*0.08)*600; z=70 + math.sin(i*0.18)*120 + max(0, math.sin((i-18)*0.10))*90
        nx=(i+1)*7500.0; ny=math.sin((i+1)*0.25)*1300 + math.sin((i+1)*0.08)*600; yaw=math.degrees(math.atan2(ny-y,nx-x)) if i<17 else 0
        rot=u.Rotator(0,yaw,0)
        # cover blue void with visible green shoulders adjacent to road; keep road center unobstructed
        for side in [-1,1]:
            g=u.EditorLevelLibrary.spawn_actor_from_object(cube,u.Vector(x,y+side*1000,z+8),rot); g.set_actor_label(f'Fill_GreenSide_{i}_{side}'); g.set_actor_scale3d(u.Vector(80,6.5,0.07)); g.static_mesh_component.set_material(0,grass)
            sh=u.EditorLevelLibrary.spawn_actor_from_object(cube,u.Vector(x,y+side*520,z+18),rot); sh.set_actor_label(f'Fill_Shoulder_{i}_{side}'); sh.set_actor_scale3d(u.Vector(80,1.0,0.05)); sh.static_mesh_component.set_material(0,shoulder)
    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(),'/Game/Zafira/Maps/ZafiraPlayableTrack')
    report={'success':True,'save_map':ok,'note':'Filled visible sky/void gaps beside road with bright green terrain and grey shoulders.'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'fill_track_gaps_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')