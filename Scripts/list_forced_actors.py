import unreal as u, pathlib, json
u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraLongTrack')
rows=[]
for a in u.EditorLevelLibrary.get_all_level_actors():
    lab=a.get_actor_label()
    if lab.startswith('CAMERA_TEST_') or lab.startswith('FORCED_VISIBLE_'):
        loc=a.get_actor_location(); sc=a.get_actor_scale3d(); rows.append({'label':lab,'class':a.get_class().get_name(),'loc':[loc.x,loc.y,loc.z],'scale':[sc.x,sc.y,sc.z]})
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/forced_actors.json'); path.write_text(json.dumps(rows,indent=2)); print(path)
