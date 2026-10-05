import unreal as u, pathlib, json, traceback
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
r={}
try:
    meta=json.loads((ROOT/'SourceArt/LongTrack/long_track_meta.json').read_text()); sx,sy,sz=meta['start']; yaw=meta['start_yaw_deg']
    world=u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraLongTrack')
    actor_sub=u.get_editor_subsystem(u.EditorActorSubsystem)
    changed=[]
    for a in actor_sub.get_all_level_actors():
        cls=a.get_class().get_name(); label=a.get_actor_label()
        if cls=='PlayerStart' or 'PlayerStart' in label:
            a.set_actor_location(u.Vector(sx,sy,sz+650), False, False)
            a.set_actor_rotation(u.Rotator(0,yaw,0), False)
            changed.append({'label':label,'class':cls,'loc':str(a.get_actor_location())})
        # remove manually-placed pawn at start; GameMode should spawn exactly one pawn, not collide with placed one
        if label.startswith('Player_Zafira_Start'):
            actor_sub.destroy_actor(a); changed.append({'removed':label})
    ok=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraLongTrack')
    r={'success':bool(ok),'changed':changed,'start':[sx,sy,sz+650],'yaw':yaw}
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
(ROOT/'Scripts/fix_spawn_report.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,default=str))
assert r.get('success'), r