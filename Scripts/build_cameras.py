import unreal as u,json,pathlib,shutil,traceback
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive');S=R/'Scripts';E=u.EditorAssetLibrary;L=u.BlueprintEditorLibrary;G=u.BlueprintGraphEditor
base='/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase';car='/Game/Zafira/BP_Zafira'
backup=S/'camera_backup';backup.mkdir(exist_ok=True)
for rel in ['Content/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase.uasset','Content/Zafira/BP_Zafira.uasset']:
 src=R/rel;dest=backup/src.name
 if not dest.exists():shutil.copy2(src,dest)
r={};pending=[]
def link(a,b):
 assert a.is_valid() and b.is_valid(),f'Invalid pins {a} {b}'
 assert a.try_create_connection(b),f'Cannot link {a} {b}'
def val(n,p,v):
 pin=n.find_input_pin(p);assert pin.is_valid(),f'{n.get_node_title()} no {p}'
 ok=pin.set_pin_value(str(v));assert ok is not False or pin.get_pin_value()==str(v),f'Bad literal {p} {v}: result={ok} actual={pin.get_pin_value()}'
def call(g,path,**values):
 n=g.add_call_function_node('/Script/Engine.'+path);assert n,path
 for p,v in values.items():pending.append((n,p,v))
 return n
def get(g,name):return g.add_get_member_variable_node(name).find_result_pin()
def result(n):return n.find_result_pin()
def setvar(g,name,value=None):
 n=g.add_set_member_variable_node(name)
 if value is not None:val(n,name,value)
 return n
def chain(pin,n):link(pin,n.find_execute_pin());return n.find_then_pin()
def target(g,n,name):link(get(g,name),n.find_self_pin())
try:
 bp=u.load_asset(base);z=u.load_asset(car)
 c=u.get_default_object(E.load_blueprint_class(car));m=c.get_component_by_class(u.ChaosWheeledVehicleMovementComponent)
 scalar={p:m.get_editor_property(p) for p in ['mass','drag_coefficient','chassis_width','chassis_height']};structs={p:m.get_editor_property(p).export_text() for p in ['engine_setup','transmission_setup','differential_setup']};wheels=[s.export_text() for s in m.get_editor_property('wheel_setups')]
 for name in ['ZafiraCycleCamera','ZafiraCameraLook','ZafiraApplyCameraLook']:
  if name in [str(x) for x in L.list_graph_names(bp)]:L.remove_function_graph(bp,name)
 event=G.get_graph_editor_by_name(bp,'EventGraph');ns={n.get_name():n for n in event.list_all_nodes()}
 for name,typ,value in [('ZafiraCameraMode','int','0'),('ZafiraLookYaw','real','0'),('ZafiraLookPitch','real','0')]:
  if name not in L.list_member_variable_names(bp,False):assert event.add_member_variable(name,L.get_basic_type_by_name(typ),value)
 # Eliminate old two-camera flip-flop, yaw-only input and auto-recentering.
 ns['K2Node_EnhancedInputAction_7'].find_output_pin('Triggered').break_pin_links()
 ns['K2Node_EnhancedInputAction_3'].find_output_pin('Triggered').break_pin_links()
 ns['K2Node_CallFunction_23'].find_then_pin().break_pin_links()
 # Three-mode switch uses the existing EnhancedInput Tab action's Started edge.
 g=G.create_and_edit_function_graph(bp,'ZafiraCycleCamera');p=g.find_graph_entry_pin()
 add=call(g,'KismetMathLibrary.Add_IntInt',B=1);link(get(g,'ZafiraCameraMode'),add.find_input_pin('A'))
 mod=call(g,'KismetMathLibrary.Percent_IntInt',B=3);link(result(add),mod.find_input_pin('A'))
 st=setvar(g,'ZafiraCameraMode');link(result(mod),st.find_input_pin('ZafiraCameraMode'));p=chain(p,st)
 for v in ['ZafiraLookYaw','ZafiraLookPitch']:p=chain(p,setvar(g,v,0))
 eq=call(g,'KismetMathLibrary.EqualEqual_IntInt',B=2);link(get(g,'ZafiraCameraMode'),eq.find_input_pin('A'))
 b=g.add_branch_node();link(result(eq),b.find_condition_pin());p=chain(p,b)
 for interior,start in [(True,b.find_then_pin()),(False,b.find_else_pin())]:
  p=start
  for cam,active in [('BackCamera',not interior),('FrontCamera',interior)]:
   n=call(g,'ActorComponent.SetActive',bNewActive=str(active).lower(),bReset='false');target(g,n,cam);p=chain(p,n)
  if not interior:
   eq1=call(g,'KismetMathLibrary.EqualEqual_IntInt',B=1);link(get(g,'ZafiraCameraMode'),eq1.find_input_pin('A'))
   sel=call(g,'KismetMathLibrary.SelectFloat',A=1000,B=650);link(result(eq1),sel.find_input_pin('bPickA'))
   st=g.add_set_member_variable_node('TargetArmLength','/Script/Engine.SpringArmComponent');target(g,st,'BackSpringArm');link(result(sel),st.find_input_pin('TargetArmLength'));p=chain(p,st)
 # Mouse deltas captured in native runtime Blueprint tick. No Python needed in game.
 g=G.create_and_edit_function_graph(bp,'ZafiraCameraLook');p=g.find_graph_entry_pin()
 local=call(g,'Pawn.IsLocallyControlled');branch=g.add_branch_node();link(result(local),branch.find_condition_pin());chain(p,branch);p=branch.find_then_pin()
 pc=call(g,'GameplayStatics.GetPlayerController',PlayerIndex=0);delta=call(g,'PlayerController.GetInputMouseDelta');link(result(pc),delta.find_self_pin())
 for var,axis,scale in [('ZafiraLookYaw','DeltaX',0.25),('ZafiraLookPitch','DeltaY',-0.25)]:
  mul=call(g,'KismetMathLibrary.Multiply_DoubleDouble',B=scale);link(delta.find_output_pin(axis),mul.find_input_pin('A'))
  add=call(g,'KismetMathLibrary.Add_DoubleDouble');link(get(g,var),add.find_input_pin('A'));link(result(mul),add.find_input_pin('B'))
  if axis=='DeltaX':clamp=call(g,'KismetMathLibrary.NormalizeAxis');link(result(add),clamp.find_input_pin('Angle'))
  else:clamp=call(g,'KismetMathLibrary.FClamp',Min=-65,Max=50);link(result(add),clamp.find_input_pin('Value'))
  st=setvar(g,var);link(result(clamp),st.find_input_pin(var));p=chain(p,st)
 for arm in ['BackSpringArm','FrontSpringArm']:
  rot=call(g,'KismetMathLibrary.MakeRotator',Roll=0);link(get(g,'ZafiraLookPitch'),rot.find_input_pin('Pitch'));link(get(g,'ZafiraLookYaw'),rot.find_input_pin('Yaw'))
  n=call(g,'SceneComponent.K2_SetRelativeRotation',bSweep='false',bTeleport='true');target(g,n,arm);link(result(rot),n.find_input_pin('NewRotation'));p=chain(p,n)
 # Make generated functions callable, then connect original runtime events.
 for n,key,value in pending:val(n,key,value)
 L.compile_blueprint(bp)
 event=G.get_graph_editor_by_name(bp,'EventGraph');ns={n.get_name():n for n in event.list_all_nodes()}
 for fun,node,pin in [('ZafiraCycleCamera','K2Node_EnhancedInputAction_7','Started'),('ZafiraCameraLook','K2Node_CallFunction_23','then')]:
  n=event.add_call_function_node(base+'.BP_VehicleAdvPawnBase_C:'+fun);assert n,fun
  link(ns[node].find_output_pin(pin),n.find_execute_pin())
 L.compile_blueprint(bp);L.compile_blueprint(z)
 errors=[]
 for asset in [bp,z]:
  for name in L.list_graph_names(asset):errors += [n.get_node_title() for n in G.get_graph_editor_by_name(asset,name).list_nodes_with_errors()]
 assert not errors,errors
 # Camera-only component defaults, after compilation.
 ss=u.get_engine_subsystem(u.SubobjectDataSubsystem);lib=u.SubobjectDataBlueprintFunctionLibrary
 for h in ss.k2_gather_subobject_data_for_blueprint(bp):
  o=lib.get_object(lib.get_data(h));name=o.get_name()
  if isinstance(o,u.SpringArmComponent):
   o.modify();o.use_pawn_control_rotation=False;o.inherit_pitch=False;o.inherit_yaw=True;o.inherit_roll=False
   if name.startswith('FrontSpringArm'):
    o.set_editor_property('relative_location',u.Vector(20,-38,125));o.target_arm_length=0;o.do_collision_test=False;o.enable_camera_lag=False;o.enable_camera_rotation_lag=False
   if name.startswith('BackSpringArm'):o.target_arm_length=650
  if isinstance(o,u.CameraComponent):o.use_pawn_control_rotation=False
 # Restore all pre-existing physics values after class reconstruction.
 c=u.get_default_object(E.load_blueprint_class(car));c.modify();m=c.get_component_by_class(u.ChaosWheeledVehicleMovementComponent);m.modify()
 c.get_component_by_class(u.SkeletalMeshComponent).set_skeletal_mesh_asset(u.load_asset('/Game/Zafira/Meshes/SKM_ZafiraAligned'))
 for p,v in scalar.items():m.set_editor_property(p,v)
 for p,text in structs.items():
  v=m.get_editor_property(p);assert v.import_text(text);m.set_editor_property(p,v)
 ws=[]
 for text in wheels:
  v=u.ChaosWheelSetup();assert v.import_text(text);ws.append(v)
 m.set_editor_property('wheel_setups',ws)
 for asset in [bp,z]:assert E.save_loaded_asset(asset,False)
 r={'success':True,'errors':errors,'mode_order':['Close chase 650cm','Far chase 1000cm','Driver seat'],'pitch_limits':[-65,50],'sensitivity':0.25,'driver_eye':[20,-38,125],'scalar_preserved':scalar,'structs_preserved':structs,'wheel_setups':wheels}
except:
 r['error']=traceback.format_exc();u.log_error(r['error'])
finally:(S/'camera_build_report.json').write_text(json.dumps(r,indent=2))
assert r.get('success'),r
