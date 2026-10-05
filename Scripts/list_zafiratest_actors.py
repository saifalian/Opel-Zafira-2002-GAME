import unreal as u, pathlib, json, traceback
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/zafiratest_actors.json')
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraTest')
    rows=[]
    for a in u.EditorLevelLibrary.get_all_level_actors():
        cls=a.get_class().get_name(); lab=a.get_actor_label();
        if 'Zafira' in cls or 'Zafira' in lab or 'Vehicle' in cls or 'Pawn' in cls or cls=='PlayerStart':
            loc=a.get_actor_location(); row={'label':lab,'name':a.get_name(),'class':cls,'loc':[loc.x,loc.y,loc.z]}
            for p in ['auto_possess_player','auto_receive_input']:
                try: row[p]=str(a.get_editor_property(p))
                except Exception as e: row[p]='ERR '+str(e)
            rows.append(row)
    path.write_text(json.dumps({'success':True,'actors':rows},indent=2,default=str))
except Exception:
    path.write_text(json.dumps({'success':False,'error':traceback.format_exc()},indent=2))
print(path)
