import unreal as u,time,json,pathlib,traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts');E=u.EditorAssetLibrary;L=u.BlueprintEditorLibrary;G=u.BlueprintGraphEditor
u.EditorLevelLibrary.load_level('/Game/Zafira/Maps/ZafiraTest');cl=E.load_blueprint_class('/Game/Zafira/BP_Zafira');bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase');sub=u.get_editor_subsystem(u.LevelEditorSubsystem)
out={'test':'Independent reload + PIE physics with native Blueprint function calls and Chaos throttle/brake setters; not OS keyboard verification','rows':[],'checks':{}};state={'wall':time.time(),'t':0,'busy':False,'started':False,'phase':None}
c=u.get_default_object(cl);m=c.get_component_by_class(u.ChaosWheeledVehicleMovementComponent)
out['persisted']={'graphs':list(L.list_graph_names(bp)),'mass':m.get_editor_property('mass'),'drag':m.get_editor_property('drag_coefficient'),'transmission':m.get_editor_property('transmission_setup').export_text(),'wheels':[s.export_text() for s in m.get_editor_property('wheel_setups')],'mesh':c.get_component_by_class(u.SkeletalMeshComponent).get_skeletal_mesh_asset().get_path_name(),'errors':[n.get_node_title() for name in L.list_graph_names(bp) for n in G.get_graph_editor_by_name(bp,name).list_nodes_with_errors()]}
def finish(error=None):
 out['error']=error;(S/'transmission_runtime_report.json').write_text(json.dumps(out,indent=2,default=str));u.unregister_slate_post_tick_callback(handle);sub.editor_request_end_play();u.SystemLibrary.quit_editor()
def tick(dt):
 if state['busy']:return
 state['busy']=True
 try:
  if time.time()-state['wall']>150:finish('wall timeout');return
  if not state['started']:state['started']=True;sub.editor_play_simulate();return
  world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
  if not world:return
  cars=u.GameplayStatics.get_all_actors_of_class(world,cl)
  if not cars:return
  p=cars[0];m=p.get_component_by_class(u.ChaosWheeledVehicleMovementComponent);pc=u.GameplayStatics.get_player_controller(world,0)
  if pc and not state.get('possessed'):pc.possess(p);state['possessed']=True
  m.set_requires_controller_for_inputs(False) if hasattr(m,'set_requires_controller_for_inputs') else m.set_editor_property('requires_controller_for_inputs',False)
  state['t']+=dt;t=state['t'];thr=0;brk=0
  phase=0 if t<2 else 1 if t<16 else 2 if t<23 else 3 if t<26 else 4 if t<29 else 5 if t<31 else 6 if t<39 else 7 if t<42 else 8 if t<45 else 9
  if phase!=state['phase']:
   state['phase']=phase
   if phase==2:
    gears={r['gear'] for r in out['rows'] if r['phase']==1};assert len(gears)>=2 and max(gears)>=2,gears;out['checks']['auto_shift_gears']=sorted(gears)
    p.call_method('ZafiraToggleTransmission');assert p.get_editor_property('ZafiraManualTransmission');assert not m.get_use_auto_gears();assert not m.get_editor_property('reverse_as_brake')
    while p.get_editor_property('ZafiraRequestedGear')>1:p.call_method('ZafiraShiftDown')
   if phase==3:
    rows=[r for r in out['rows'] if r['phase']==2 and r['t']>17];assert rows and all(r['gear']==1 and not r['auto'] for r in rows);out['checks']['manual_first_held_seconds']=rows[-1]['t']-rows[0]['t'];p.call_method('ZafiraShiftUp')
   if phase==4:
    assert m.get_current_gear()==2;mgear=m.get_current_gear();p.call_method('ZafiraShiftDown');out['checks']['upshift']=mgear
   if phase==5:
    assert m.get_current_gear()==1;out['checks']['downshift']=1;p.call_method('ZafiraShiftDown');assert p.get_editor_property('ZafiraRequestedGear')==0
    assert abs(m.get_forward_speed())>100;p.call_method('ZafiraShiftDown');assert p.get_editor_property('ZafiraRequestedGear')==0;out['checks']['reverse_rejected_while_moving']=True
   if phase==6:
    assert m.get_current_gear()==0;out['checks']['neutral_held_under_throttle']=True
   if phase==7:
    assert abs(m.get_forward_speed())<100,m.get_forward_speed();assert m.get_current_gear()==0;out['checks']['braking_did_not_select_reverse']=True;p.call_method('ZafiraShiftDown')
   if phase==8:
    assert m.get_current_gear()==-1;assert m.get_forward_speed()<0;out['checks']['reverse_drives_with_positive_throttle']=True
   if phase==9:
    p.call_method('ZafiraToggleTransmission');assert m.get_use_auto_gears();assert m.get_editor_property('reverse_as_brake');out['checks']['returned_to_auto']=True;finish();return
  if phase==0:brk=1
  if phase in [1,2,3,4,5,7]:thr=1
  if phase in [6,8]:brk=1
  m.set_throttle_input(thr);m.set_brake_input(brk);m.set_steering_input(0)
  if not out['rows'] or t-out['rows'][-1]['t']>.1:out['rows'].append({'t':t,'phase':phase,'gear':m.get_current_gear(),'target':m.get_target_gear(),'requested':p.get_editor_property('ZafiraRequestedGear'),'auto':m.get_use_auto_gears(),'reverse_as_brake':m.get_editor_property('reverse_as_brake'),'speed_kmh':m.get_forward_speed()*.036,'rpm':m.get_engine_rotation_speed()})
 except:finish(traceback.format_exc())
 finally:state['busy']=False
handle=u.register_slate_post_tick_callback(tick)
