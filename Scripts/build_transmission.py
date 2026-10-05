import unreal as u,json,pathlib,shutil,traceback
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive');S=R/'Scripts';E=u.EditorAssetLibrary;L=u.BlueprintEditorLibrary;G=u.BlueprintGraphEditor
base='/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase';car='/Game/Zafira/BP_Zafira';MC='/Script/ChaosVehicles.ChaosVehicleMovementComponent'
backup=S/'transmission_backup';backup.mkdir(exist_ok=True)
for rel in ['Content/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase.uasset','Content/Zafira/BP_Zafira.uasset']:
 src=R/rel;dest=backup/src.name
 if not dest.exists():shutil.copy2(src,dest)
r={};pending=[]
def link(a,b):
 assert a.is_valid() and b.is_valid(),'Invalid pins'
 assert a.try_create_connection(b),'Cannot connect pins'
def val(n,p,v):
 pin=n.find_input_pin(p);assert pin.is_valid(),n.get_node_title()+':'+p
 ok=pin.set_pin_value(str(v));assert ok is not False or pin.get_pin_value()==str(v),(p,v,pin.get_pin_value())
def call(g,path,**vs):
 n=g.add_call_function_node(path if path.startswith('/') else '/Script/Engine.'+path);assert n,path
 for p,v in vs.items():pending.append((n,p,v))
 return n
def get(g,name):return g.add_get_member_variable_node(name).find_result_pin()
def result(n):return n.find_result_pin()
def chain(p,n):link(p,n.find_execute_pin());return n.find_then_pin()
def st(g,name,value=None):
 n=g.add_set_member_variable_node(name)
 if value is not None:pending.append((n,name,value))
 return n
def move(g,fn,**vs):
 n=call(g,MC+'.'+fn,**vs);link(get(g,'Chaos Wheeled Vehicle Movement Component'),n.find_self_pin());return n
def branch(g,p,cond):
 b=g.add_branch_node();link(cond,b.find_condition_pin());chain(p,b);return b
def math(g,fn,**vs):return call(g,'KismetMathLibrary.'+fn,**vs)
def notify(g,p,text,key='ZafiraTransmissionNotice',duration=2):
 n=call(g,'KismetSystemLibrary.PrintString',InString=text,bPrintToScreen='true',bPrintToLog='false',Duration=duration,Key=key);return chain(p,n)
def compiled():
 global pending
 for n,p,v in pending:val(n,p,v)
 pending=[];L.compile_blueprint(bp)
try:
 bp=u.load_asset(base);z=u.load_asset(car);c=u.get_default_object(E.load_blueprint_class(car));m=c.get_component_by_class(u.ChaosWheeledVehicleMovementComponent)
 scalar={p:m.get_editor_property(p) for p in ['mass','drag_coefficient','chassis_width','chassis_height']};structs={p:m.get_editor_property(p).export_text() for p in ['engine_setup','transmission_setup','differential_setup']};wheels=[s.export_text() for s in m.get_editor_property('wheel_setups')]
 names=['ZafiraToggleTransmission','ZafiraShiftUp','ZafiraShiftDown','ZafiraTransmissionInput']
 for name in names:
  if name in L.list_graph_names(bp):L.remove_function_graph(bp,name)
 event=G.get_graph_editor_by_name(bp,'EventGraph')
 for name,typ,value in [('ZafiraManualTransmission','bool','false'),('ZafiraRequestedGear','int','1')]:
  if name not in L.list_member_variable_names(bp,False):assert event.add_member_variable(name,L.get_basic_type_by_name(typ),value)
 # Toggle captures actual gear; disable Chaos automatic and brake-as-reverse together.
 g=G.create_and_edit_function_graph(bp,names[0]);p=g.find_graph_entry_pin()
 flip=math(g,'Not_PreBool');link(get(g,'ZafiraManualTransmission'),flip.find_input_pin('A'));s=st(g,'ZafiraManualTransmission');link(result(flip),s.find_input_pin('ZafiraManualTransmission'));p=chain(p,s)
 b=branch(g,p,get(g,'ZafiraManualTransmission'))
 for manual,p in [(True,b.find_then_pin()),(False,b.find_else_pin())]:
  cur=move(g,'GetCurrentGear');s=st(g,'ZafiraRequestedGear');link(result(cur),s.find_input_pin('ZafiraRequestedGear'));p=chain(p,s)
  p=chain(p,move(g,'SetUseAutomaticGears',bUseAuto=str(not manual).lower()))
  s=call(g,'KismetSystemLibrary.SetBoolPropertyByName',PropertyName='bReverseAsBrake',Value=str(not manual).lower());link(get(g,'Chaos Wheeled Vehicle Movement Component'),s.find_input_pin('Object'));p=chain(p,s)
  if manual:
   n=move(g,'SetTargetGear',bImmediate='true');link(get(g,'ZafiraRequestedGear'),n.find_input_pin('GearNum'));p=chain(p,n)
  notify(g,p,'MANUAL: Q down / E up | R - N - 1..5 | W throttle, S brake' if manual else 'AUTOMATIC: W drive / S brake and reverse | M manual')
 # Sequential manual shifts including neutral, with direction-change lock above 1m/s.
 for fun,delta in [(names[1],1),(names[2],-1)]:
  g=G.create_and_edit_function_graph(bp,fun);p=g.find_graph_entry_pin();b=branch(g,p,get(g,'ZafiraManualTransmission'));p=b.find_then_pin()
  add=math(g,'Add_IntInt',B=delta);link(get(g,'ZafiraRequestedGear'),add.find_input_pin('A'));clamp=math(g,'Clamp',Min=-1,Max=5);link(result(add),clamp.find_input_pin('Value'))
  rev=math(g,'EqualEqual_IntInt',B=-1);link(result(clamp),rev.find_input_pin('A'));was=math(g,'EqualEqual_IntInt',B=-1);link(get(g,'ZafiraRequestedGear'),was.find_input_pin('A'));either=math(g,'BooleanOR');link(result(rev),either.find_input_pin('A'));link(result(was),either.find_input_pin('B'))
  speed=move(g,'GetForwardSpeed');ab=math(g,'Abs');link(result(speed),ab.find_input_pin('A'));fast=math(g,'Greater_DoubleDouble',B=100);link(result(ab),fast.find_input_pin('A'));blocked=math(g,'BooleanAND');link(result(either),blocked.find_input_pin('A'));link(result(fast),blocked.find_input_pin('B'));b=branch(g,p,result(blocked));notify(g,b.find_then_pin(),'Stop before selecting or leaving reverse (below 3.6 km/h)')
  s=st(g,'ZafiraRequestedGear');link(result(clamp),s.find_input_pin('ZafiraRequestedGear'));p=chain(b.find_else_pin(),s)
  p=chain(p,move(g,'SetUseAutomaticGears',bUseAuto='false'));n=move(g,'SetTargetGear',bImmediate='true');link(get(g,'ZafiraRequestedGear'),n.find_input_pin('GearNum'));p=chain(p,n)
  conv=call(g,'KismetStringLibrary.Conv_IntToString');link(get(g,'ZafiraRequestedGear'),conv.find_input_pin('InInt'));cat=call(g,'KismetStringLibrary.Concat_StrStr',A='MANUAL gear: ');link(result(conv),cat.find_input_pin('B'));n=call(g,'KismetSystemLibrary.PrintString',bPrintToScreen='true',bPrintToLog='false',Duration=2,Key='ZafiraTransmissionNotice');link(result(cat),n.find_input_pin('InString'));chain(p,n)
 compiled()
 # Native compiled Blueprint keyboard edge polling, not editor Python tick.
 g=G.create_and_edit_function_graph(bp,names[3]);p=g.find_graph_entry_pin();local=call(g,'Pawn.IsLocallyControlled');b=branch(g,p,result(local));p=b.find_then_pin();pc=call(g,'GameplayStatics.GetPlayerController',PlayerIndex=0)
 for key,fun in [('M',names[0]),('E',names[1]),('Q',names[2])]:
  test=call(g,'PlayerController.WasInputKeyJustPressed',Key='(KeyName="'+key+'")');link(result(pc),test.find_self_pin());b=branch(g,p,result(test));n=call(g,base+'.BP_VehicleAdvPawnBase_C:'+fun);chain(b.find_then_pin(),n)
  # Merge true and false to next check using a shared executable node.
  merge=call(g,'KismetSystemLibrary.PrintString',InString='',bPrintToScreen='false',bPrintToLog='false',Duration=0);link(n.find_then_pin(),merge.find_execute_pin());link(b.find_else_pin(),merge.find_execute_pin());p=merge.find_then_pin()
 # Hold manual target even if other template logic later requests an automatic gear.
 b=branch(g,p,get(g,'ZafiraManualTransmission'));p=b.find_then_pin();p=chain(p,move(g,'SetUseAutomaticGears',bUseAuto='false'));n=move(g,'SetTargetGear',bImmediate='true');link(get(g,'ZafiraRequestedGear'),n.find_input_pin('GearNum'));p=chain(p,n)
 for manual,p in [(True,p),(False,b.find_else_pin())]:
  gear=move(g,'GetCurrentGear');conv=call(g,'KismetStringLibrary.Conv_IntToString');link(result(gear),conv.find_input_pin('InInt'));cat=call(g,'KismetStringLibrary.Concat_StrStr',A=('MANUAL' if manual else 'AUTO')+' | gear ');link(result(conv),cat.find_input_pin('B'));cat2=call(g,'KismetStringLibrary.Concat_StrStr',B=' (-1=R, 0=N) | M mode | Q/E shift');link(result(cat),cat2.find_input_pin('A'));n=call(g,'KismetSystemLibrary.PrintString',bPrintToScreen='true',bPrintToLog='false',Duration=0.15,Key='ZafiraTransmissionStatus');link(result(cat2),n.find_input_pin('InString'));chain(p,n)
 compiled();event=G.get_graph_editor_by_name(bp,'EventGraph');cam=next(n for n in event.list_all_nodes() if n.get_node_title()=='ZafiraCameraLook');cam.find_then_pin().break_pin_links();n=call(event,base+'.BP_VehicleAdvPawnBase_C:'+names[3]);chain(cam.find_then_pin(),n)
 compiled();L.compile_blueprint(z)
 errors=[]
 for asset in [bp,z]:
  for name in L.list_graph_names(asset):errors += [n.get_node_title() for n in G.get_graph_editor_by_name(asset,name).list_nodes_with_errors()]
 assert not errors,errors
 c=u.get_default_object(E.load_blueprint_class(car));c.modify();m=c.get_component_by_class(u.ChaosWheeledVehicleMovementComponent);m.modify();c.get_component_by_class(u.SkeletalMeshComponent).set_skeletal_mesh_asset(u.load_asset('/Game/Zafira/Meshes/SKM_ZafiraAligned'))
 for p,v in scalar.items():m.set_editor_property(p,v)
 for p,text in structs.items():
  v=m.get_editor_property(p);assert v.import_text(text);m.set_editor_property(p,v)
 ws=[]
 for text in wheels:
  v=u.ChaosWheelSetup();assert v.import_text(text);ws.append(v)
 m.set_editor_property('wheel_setups',ws)
 for asset in [bp,z]:assert E.save_loaded_asset(asset,False)
 r={'success':True,'errors':errors,'functions':names,'scalar_preserved':scalar,'structs_preserved':structs,'wheel_setups':wheels,'implementation':'Native Blueprint PlayerController key-edge polling on pawn tick. No Python needed at runtime. Manual sequential selection, not clutch simulation.'}
except:r['error']=traceback.format_exc();u.log_error(r['error'])
finally:(S/'transmission_build_report.json').write_text(json.dumps(r,indent=2))
assert r.get('success'),r
