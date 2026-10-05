import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
report={}
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraLongTrack')
    actors=u.EditorLevelLibrary.get_all_level_actors()
    changed=[]
    for a in actors:
        if a.get_class().get_name()=='PlayerStart':
            a.modify()
            a.set_actor_transform(u.Transform(u.Vector(84724.3408,-163.0547,2500.0), u.Rotator(0,0,0), u.Vector(1,1,1)), False, False)
            changed.append(a.get_name())
    ok1=u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    ok2=u.EditorLevelLibrary.save_current_level()
    report={'success':True,'changed':changed,'save_dirty':ok1,'save_current_level':ok2}
except Exception:
    report={'success':False,'error':traceback.format_exc()}
(S/'force_move_playerstart_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report))
assert report.get('success')