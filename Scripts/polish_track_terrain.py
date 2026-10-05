import unreal as u, pathlib, json, traceback, math
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; tools=u.AssetToolsHelpers.get_asset_tools()
report={}
def mat(name,color):
    m=E.load_asset(f'/Game/Zafira/LongTrack/Materials/{name}') or tools.create_asset(name,'/Game/Zafira/LongTrack/Materials',u.Material,u.MaterialFactoryNew())
    m.modify();
    b=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,0); b.constant=u.LinearColor(*color,1); u.MaterialEditingLibrary.connect_material_property(b,'RGB',u.MaterialProperty.MP_BASE_COLOR)
    e=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-500,220); e.constant=u.LinearColor(color[0]*.12,color[1]*.12,color[2]*.12,1); u.MaterialEditingLibrary.connect_material_property(e,'RGB',u.MaterialProperty.MP_EMISSIVE_COLOR)
    u.MaterialEditingLibrary.recompile_material(m); E.save_loaded_asset(m,False); return m
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraPlayableTrack')
    cube=E.load_asset('/Engine/BasicShapes/Cube.Cube'); cyl=E.load_asset('/Engine/BasicShapes/Cylinder.Cylinder'); cone=E.load_asset('/Engine/BasicShapes/Cone.Cone')
    grass=mat('M_TRACK_SIDE_GRASS_RICH',(0.03,0.42,0.07)); soil=mat('M_TRACK_SIDE_DIRT',(0.30,0.20,0.11)); tree=E.load_asset('/Game/Zafira/LongTrack/Materials/M_BEAUTIFUL_TREE_LEAF'); trunk=E.load_asset('/Game/Zafira/LongTrack/Materials/M_BEAUTIFUL_TREE_TRUNK')
    # remove template checker floors/blocks so screenshots don't look like prototype grid
    removed=[]
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        lab=a.get_actor_label()
        if a.get_class().get_name()=='StaticMeshActor' and not (lab.startswith('BT_') or lab.startswith('Scenery_') or lab.startswith('Terrain_')):
            removed.append(lab); u.EditorLevelLibrary.destroy_actor(a)
    # add rich terrain slabs and more visible trees/buildings near first 1.5km where user sees them
    for i in range(18):
        x=i*7500.0; y=math.sin(i*0.25)*1300 + math.sin(i*0.08)*600; z=70 + math.sin(i*0.18)*120 + max(0, math.sin((i-18)*0.10))*90
        yaw=0
        if i<71:
            nx=(i+1)*7500.0; ny=math.sin((i+1)*0.25)*1300 + math.sin((i+1)*0.08)*600; yaw=math.degrees(math.atan2(ny-y,nx-x))
        rot=u.Rotator(0,yaw,0)
        a=u.EditorLevelLibrary.spawn_actor_from_object(cube,u.Vector(x,y,z-42),rot); a.set_actor_label(f'Terrain_Green_Base_{i:02d}'); a.set_actor_scale3d(u.Vector(82,18,0.18)); a.static_mesh_component.set_material(0,grass)
        d=u.EditorLevelLibrary.spawn_actor_from_object(cube,u.Vector(x,y,z-37),rot); d.set_actor_label(f'Terrain_Dirt_Shoulder_{i:02d}'); d.set_actor_scale3d(u.Vector(82,5.2,0.08)); d.static_mesh_component.set_material(0,soil)
        if i%2==0:
            for side in [-1,1]:
                for n in range(2):
                    tx=x+n*850; ty=y+side*(850+n*270); tz=z+115
                    tr=u.EditorLevelLibrary.spawn_actor_from_object(cyl,u.Vector(tx,ty,tz),u.Rotator(0,0,0)); tr.set_actor_label(f'Scenery_TreeTrunk_{i}_{side}_{n}'); tr.set_actor_scale3d(u.Vector(.35,.35,2.6)); tr.static_mesh_component.set_material(0,trunk)
                    lf=u.EditorLevelLibrary.spawn_actor_from_object(cone,u.Vector(tx,ty,tz+280),u.Rotator(0,0,0)); lf.set_actor_label(f'Scenery_TreeLeaf_{i}_{side}_{n}'); lf.set_actor_scale3d(u.Vector(1.7,1.7,2.5)); lf.static_mesh_component.set_material(0,tree)
    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(),'/Game/Zafira/Maps/ZafiraPlayableTrack')
    report={'success':True,'removed_template_actors':removed[:30],'save_map':ok,'note':'Removed checker template floor/blocks and added green terrain/dirt/tree scenery near playable camera path.'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'polish_track_terrain_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')