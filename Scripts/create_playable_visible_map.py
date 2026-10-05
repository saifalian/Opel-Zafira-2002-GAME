import unreal as u, pathlib, json, traceback, math
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; tools=u.AssetToolsHelpers.get_asset_tools()
report={}
def make_mat(name,color):
    path=f'/Game/Zafira/LongTrack/Materials/{name}'
    m=E.load_asset(path) or tools.create_asset(name,'/Game/Zafira/LongTrack/Materials',u.Material,u.MaterialFactoryNew())
    m.modify(); m.set_editor_property('shading_model', u.MaterialShadingModel.MSM_UNLIT); m.set_editor_property('two_sided', True)
    c=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,0); c.constant=u.LinearColor(*color,1)
    u.MaterialEditingLibrary.connect_material_property(c,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
    u.MaterialEditingLibrary.recompile_material(m); E.save_loaded_asset(m,False); return m
try:
    world = u.EditorLoadingAndSavingUtils.new_map_from_template('/Engine/Maps/Templates/Template_Default', True)
    cube=E.load_asset('/Engine/BasicShapes/Cube.Cube')
    road=make_mat('M_PLAYABLE_ROAD',(0.25,0.25,0.25)); grass=make_mat('M_PLAYABLE_GRASS',(0.02,0.55,0.06)); red=make_mat('M_PLAYABLE_RED',(1.5,0,0)); white=make_mat('M_PLAYABLE_WHITE',(1.5,1.5,1.5)); yellow=make_mat('M_PLAYABLE_YELLOW',(1.5,1.2,0)); blue=make_mat('M_PLAYABLE_BLUE',(0.1,0.35,1.4))
    def add(name,loc,scale,mat):
        a=u.EditorLevelLibrary.spawn_actor_from_object(cube,loc,u.Rotator(0,0,0)); a.set_actor_label(name); a.set_actor_scale3d(scale); a.static_mesh_component.set_material(0,mat); return a
    for i in range(24):
        x=i*750.0; y=math.sin(i*.5)*420
        add(f'PLAY_ROAD_{i}',u.Vector(x,y,60),u.Vector(8,5,0.18),road)
        add(f'PLAY_GRASS_L_{i}',u.Vector(x,y-650,40),u.Vector(8,4,0.15),grass); add(f'PLAY_GRASS_R_{i}',u.Vector(x,y+650,40),u.Vector(8,4,0.15),grass)
        add(f'PLAY_CURB_L_{i}',u.Vector(x,y-290,95),u.Vector(8,.25,.25),red if i%2==0 else white); add(f'PLAY_CURB_R_{i}',u.Vector(x,y+290,95),u.Vector(8,.25,.25),white if i%2==0 else red)
        if i%3==0: add(f'PLAY_BUILD_{i}',u.Vector(x,y+1250,360),u.Vector(3,3,6),blue)
        if i%2==0: add(f'PLAY_BARRIER_{i}',u.Vector(x,y-410,170),u.Vector(8,.18,1.2),yellow); add(f'PLAY_BARRIER_R_{i}',u.Vector(x,y+410,170),u.Vector(8,.18,1.2),yellow)
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart': a.set_actor_location(u.Vector(-650,0,220),False,False); a.set_actor_rotation(u.Rotator(-5,0,0),False)
    ok1=u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    ok2=u.EditorLoadingAndSavingUtils.save_current_level()
    ok3=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraPlayableTrack')
    report={'success':True,'new_map_return':str(world),'save_dirty':ok1,'save_current_level':ok2,'save_asset':ok3,'asset_exists':E.does_asset_exist('/Game/Zafira/Maps/ZafiraPlayableTrack')}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'create_playable_visible_map_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')