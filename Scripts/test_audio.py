import unreal as u,time,json,pathlib,traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts');E=u.EditorAssetLibrary;L=u.BlueprintEditorLibrary
u.EditorLevelLibrary.load_level('/Game/Zafira/Maps/ZafiraTest');cl=E.load_blueprint_class('/Game/Zafira/BP_Zafira');bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase');sub=u.get_editor_subsystem(u.LevelEditorSubsystem)
out={'authenticity':'NOT original Opel. CC0 Joseph Sardin Iveco diesel fallback. No auditory fidelity verification.','rows':[],'checks':{},'assets':[]};state={'wall':time.time(),'t':0,'busy':False,'started':False}
for short in ['Idle','Run']:
 a=u.load_asset('/Game/Zafira/Audio/DieselFallback_'+short+'Loop');out['assets'].append({'path':a.get_path_name(),'duration':a.get_editor_property('duration'),'looping':a.get_editor_property('looping'),'channels':a.get_editor_property('num_channels')})
c=u.get_default_object(cl);m=c.get_component_by_class(u.ChaosWheeledVehicleMovementComponent)
out['persisted']={'graphs':[str(n) for n in L.list_graph_names(bp)],'mass':m.get_editor_property('mass'),'transmission':m.get_editor_property('transmission_setup').export_text(),'wheels':[s.export_text() for s in m.get_editor_property('wheel_setups')],'mesh':c.get_component_by_class(u.SkeletalMeshComponent).get_skeletal_mesh_asset().get_path_name()}
def finish(error=None):
 out['error']=error;(S/'audio_runtime_report.json').write_text(json.dumps(out,indent=2));u.unregister_slate_post_tick_callback(handle);sub.editor_request_end_play();u.SystemLibrary.quit_editor()
def tick(dt):
 if state['busy']:return
 state['busy']=True
 try:
  if time.time()-state['wall']>110:finish('wall timeout');return
  if not state['started']:state['started']=True;sub.editor_play_simulate();return
  world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
  if not world:return
  cars=u.GameplayStatics.get_all_actors_of_class(world,cl)
  if not cars:return
  p=cars[0];m=p.get_component_by_class(u.ChaosWheeledVehicleMovementComponent);pc=u.GameplayStatics.get_player_controller(world,0)
  if pc and pc.get_controlled_pawn()!=p:pc.possess(p)
  m.set_editor_property('requires_controller_for_inputs',False)
  state['t']+=dt;t=state['t'];thr=0 if t<3 or t>12 else 1
  m.set_throttle_input(thr);m.set_brake_input(1 if t<3 else 0)
  if not out['rows'] or t-out['rows'][-1]['t']>.2:
   sounds=[a for a in p.get_components_by_class(u.AudioComponent) if 'ZafiraDiesel' in a.get_name()]
   out['rows'].append({'t':t,'throttle_command':thr,'rpm':m.get_engine_rotation_speed(),'smoothed_rpm':p.get_editor_property('ZafiraAudioRPM'),'smoothed_load':p.get_editor_property('ZafiraAudioLoad'),'audio':[{'name':a.get_name(),'playing':a.is_playing(),'pitch':a.pitch_multiplier,'volume':a.volume_multiplier,'sound':a.sound.get_path_name() if a.sound else None} for a in sounds]})
  if t>18:
   rows=out['rows'];assert all(len(r['audio'])==2 and all(a['playing'] for a in r['audio']) for r in rows if r['t']>1),'Audio not continuously playing'
   for name in ['ZafiraDieselIdle','ZafiraDieselRun']:
    values=[a for r in rows for a in r['audio'] if a['name'].startswith(name)];pr=[a['pitch'] for a in values];vr=[a['volume'] for a in values];assert max(pr)-min(pr)>.1;assert max(vr)-min(vr)>.05;out['checks'][name]={'pitch_range':[min(pr),max(pr)],'volume_range':[min(vr),max(vr)],'continuously_playing':True}
   assert max(r['smoothed_load'] for r in rows)>.9 and rows[-1]['smoothed_load']<.1
   out['checks']['throttle_rise_release']=True;out['success']=True;finish()
 except:finish(traceback.format_exc())
 finally:state['busy']=False
handle=u.register_slate_post_tick_callback(tick)
