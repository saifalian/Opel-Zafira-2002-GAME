import unreal as u,time,json,pathlib,traceback
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts');u.EditorLevelLibrary.load_level('/Game/Zafira/Maps/ZafiraTest');cl=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira');sub=u.get_editor_subsystem(u.LevelEditorSubsystem);state={'start':time.time(),'stage':0,'busy':False};out={'modes':[]}
def finish(err=None):
 out['error']=err;(R/'camera_runtime_report.json').write_text(json.dumps(out,indent=2));u.unregister_slate_post_tick_callback(handle);sub.editor_request_end_play();u.SystemLibrary.quit_editor()
def tick(dt):
 if state['busy']:return
 state['busy']=True
 try:
  t=time.time()-state['start']
  if t>75:finish('timeout');return
  if state['stage']==0:
   state['stage']=1;sub.editor_play_simulate();return
  world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
  if not world:return
  cars=u.GameplayStatics.get_all_actors_of_class(world,cl)
  if not cars or t<8:return
  p=cars[0];stage=state['stage']
  if stage in [1,2,3] and t>8+(stage-1)*8:
   if stage>1:p.call_method('ZafiraCycleCamera')
   cams=p.get_components_by_class(u.CameraComponent);arms=p.get_components_by_class(u.SpringArmComponent)
   out['modes'].append({'mode':p.get_editor_property('ZafiraCameraMode'),'cameras':[{'name':c.get_name(),'active':c.is_active(),'location':str(c.get_world_location()),'rotation':str(c.get_world_rotation())} for c in cams],'arms':[{'name':a.get_name(),'length':a.target_arm_length,'location':str(a.relative_location)} for a in arms]})
   active=next(c for c in cams if c.is_active());cam=u.get_editor_subsystem(u.EditorActorSubsystem).spawn_actor_from_class(u.CameraActor,u.Vector()) if False else None
   state['stage']+=1
  if state['stage']==4:
   assert [m['mode'] for m in out['modes']]==[0,1,2]
   p.call_method('ZafiraCycleCamera');assert p.get_editor_property('ZafiraCameraMode')==0
   out['cycle_verified']=True
   pc=u.GameplayStatics.get_player_controller(world,0);assert pc;pc.possess(p)
   out['look_checks']=[]
   for yaw in [0,90,180,270,360]:
    u.SystemLibrary.execute_console_command(world,'set BP_Zafira_C ZafiraLookYaw '+str(yaw),pc);u.SystemLibrary.execute_console_command(world,'set BP_Zafira_C ZafiraLookPitch 20',pc);p.call_method('ZafiraCameraLook')
    arm=next(a for a in p.get_components_by_class(u.SpringArmComponent) if a.get_name()=='BackSpringArm');rot=arm.get_relative_rotation() if hasattr(arm,'get_relative_rotation') else arm.get_editor_property('relative_rotation')
    assert abs(((rot.yaw-yaw+180)%360)-180)<1, str(rot)
    assert abs(rot.pitch-20)<1,str(rot)
    out['look_checks'].append({'yaw_requested':yaw,'yaw_actual':rot.yaw,'pitch':rot.pitch})
   finish()
 except:finish(traceback.format_exc())
 finally:state['busy']=False
handle=u.register_slate_post_tick_callback(tick)
