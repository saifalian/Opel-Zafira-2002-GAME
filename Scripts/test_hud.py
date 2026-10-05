import unreal as u,time,json,pathlib,traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts');u.EditorLevelLibrary.load_level('/Game/Zafira/Maps/ZafiraTest');sub=u.get_editor_subsystem(u.LevelEditorSubsystem);cl=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira');state={'wall':time.time(),'t':0,'busy':False,'started':False,'shot':False};out={'rows':[]}
def finish(err=None):
 out['error']=err;out['success']=err is None;(S/'hud_runtime_report.json').write_text(json.dumps(out,indent=2,default=str));u.unregister_slate_post_tick_callback(handle);sub.editor_request_end_play();u.SystemLibrary.quit_editor()
def tick(dt):
 if state['busy']:return
 state['busy']=True
 try:
  if time.time()-state['wall']>100:finish('timeout');return
  if not state['started']:state['started']=True;sub.editor_request_begin_play();return
  w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
  if not w:return
  pc=u.GameplayStatics.get_player_controller(w,0)
  if not pc:return
  p=pc.get_controlled_pawn()
  if not p:return
  m=p.get_component_by_class(u.ChaosWheeledVehicleMovementComponent);state['t']+=dt;t=state['t']
  m.set_throttle_input(1 if 3<t<11 else 0)
  hud=pc.get_editor_property('VehicleHud')
  if not hud:return
  if not out['rows'] or t-out['rows'][-1]['t']>.5:
   out['rows'].append({'t':t,'rpm':m.get_engine_rotation_speed(),'kmh':abs(m.get_forward_speed())*.036,'gear':m.get_current_gear(),'auto':m.get_use_auto_gears(),'texts':{k:str(hud.get_editor_property(k).get_text()) for k in ['UnitLabel','SpeedLabel','GearLabel']}})
  if t>9 and not state['shot']:
   state['shot']=True;u.SystemLibrary.execute_console_command(w,'Shot SHOWUI filename=D:/blender/project/zafira/driving/hud_runtime.png',pc)
  if t>12 and not state.get('manual'):p.call_method('ZafiraToggleTransmission');state['manual']=True
  if t>16:finish()
 except:finish(traceback.format_exc())
 finally:state['busy']=False
handle=u.register_slate_post_tick_callback(tick)
