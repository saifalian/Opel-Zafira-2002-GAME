import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
report={}
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraPlayableTrack')
    # Start the vehicle already on the first asphalt section, past the gantry/seam, with clearance for wheels.
    new_loc=u.Vector(1800,0,520)
    changed=[]
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart':
            a.modify(); a.set_actor_location(new_loc,False,False); a.set_actor_rotation(u.Rotator(0,0,0),False); changed.append(a.get_name())
        # remove start gantry side posts/hanging bar near the first meters; they looked ugly and may block movement/camera
        if a.get_actor_label().startswith('BT_Start_Gantry'):
            changed.append('removed '+a.get_actor_label()); u.EditorLevelLibrary.destroy_actor(a)
    world=u.EditorLevelLibrary.get_editor_world()
    ok=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraPlayableTrack')
    report={'success':True,'playerstart':[new_loc.x,new_loc.y,new_loc.z],'changed':changed,'save_map':ok,'note':'Moved spawn onto clear asphalt past gantry/seam and removed ugly/blocking gantry.'}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'fix_spawn_on_road_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')