import unreal as u, pathlib, json
u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraLongTrack')
rows=[]
for a in u.EditorLevelLibrary.get_all_level_actors():
    if a.get_class().get_name()=='PlayerStart' or 'start' in a.get_name().lower():
        loc=a.get_actor_location(); rot=a.get_actor_rotation(); rows.append({'name':a.get_name(),'label':a.get_actor_label(),'class':a.get_class().get_name(),'loc':[loc.x,loc.y,loc.z],'rot':[rot.pitch,rot.yaw,rot.roll]})
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/playerstarts.json'); path.write_text(json.dumps(rows,indent=2)); print(path)
