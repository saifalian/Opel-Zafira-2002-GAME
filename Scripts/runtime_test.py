import unreal,json,time,traceback
ROOT='D:/unreal engine/project/ZafiraDrive'
unreal.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraTest')
state={'started':False,'t':0.,'wall':time.time(),'rows':[],'busy':False}
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
def finish(error=None):
 result={'error':error,'rows':state['rows'],'test':'PIE direct Chaos control setters, not physical keyboard injection'}
 open(ROOT+'/Scripts/runtime_telemetry.json','w').write(json.dumps(result,indent=2))
 unreal.unregister_slate_post_tick_callback(handle)
 sub.editor_request_end_play()
 unreal.SystemLibrary.quit_editor()
def tick(dt):
 if state['busy']:return
 state['busy']=True
 try:
  if time.time()-state['wall']>180:finish('wall timeout');return
  if not state['started']:
   state['started']=True;sub.editor_play_simulate();return
  worlds=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
  if not worlds:return
  pc=unreal.GameplayStatics.get_player_controller(worlds,0)
  pawn=unreal.GameplayStatics.get_player_pawn(worlds,0)
  if not pawn:
   candidates=unreal.GameplayStatics.get_all_actors_of_class(worlds,unreal.ChaosWheeledVehiclePawn)
   pawn=candidates[0] if candidates else None
  if not pawn:return
  m=pawn.get_component_by_class(unreal.ChaosWheeledVehicleMovementComponent)
  if not m:
   cls=unreal.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira')
   transform=unreal.Transform(location=unreal.Vector(0,0,150))
   pawn=unreal.GameplayStatics.begin_deferred_actor_spawn_from_class(worlds,cls,transform,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN)
   unreal.GameplayStatics.finish_spawning_actor(pawn,transform)
   pc.possess(pawn)
   m=pawn.get_component_by_class(unreal.ChaosWheeledVehicleMovementComponent)
  state['t']+=dt;t=state['t']
  if t<2:thr,brk,steer=0,1,0
  elif t<18:thr,brk,steer=1,0,0
  elif t<23:thr,brk,steer=0,1,0
  elif t<30:thr,brk,steer=.6,0,.45
  else:finish();return
  m.set_throttle_input(thr);m.set_brake_input(brk);m.set_steering_input(steer)
  if not state['rows'] or t-state['rows'][-1]['t']>.1:
   loc=pawn.get_actor_location();rot=pawn.get_actor_rotation()
   state['rows'].append({'t':t,'speed_kmh':m.get_forward_speed()*0.036,'rpm':m.get_engine_rotation_speed(),'gear':m.get_current_gear(),'x':loc.x,'y':loc.y,'z':loc.z,'yaw':rot.yaw,'throttle':thr,'brake':brk,'steer':steer,'pawn':pawn.get_class().get_path_name()})
 except Exception:finish(traceback.format_exc())
 finally:state['busy']=False
handle=unreal.register_slate_post_tick_callback(tick)
