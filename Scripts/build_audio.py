import unreal as u,json,pathlib,shutil,traceback
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive');S=R/'Scripts';E=u.EditorAssetLibrary;L=u.BlueprintEditorLibrary;G=u.BlueprintGraphEditor
base='/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase';car='/Game/Zafira/BP_Zafira'
backup=S/'audio_backup';backup.mkdir(exist_ok=True)
for rel in ['Content/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase.uasset','Content/Zafira/BP_Zafira.uasset']:
 src=R/rel;dest=backup/src.name
 if not dest.exists():shutil.copy2(src,dest)
r={'status':'building','authenticity':'NOT original Opel: Iveco Daily 3.0 CC0 Joseph Sardin BigSoundBank fallback; approximate RPM/load model, not calibrated recording RPM.'};pending=[]
(S/'audio_build_report.json').write_text(json.dumps(r,indent=2))
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
def math(g,fn,**vs):return call(g,'KismetMathLibrary.'+fn,**vs)
def compiled():
 global pending
 for n,p,v in pending:val(n,p,v)
 pending=[];L.compile_blueprint(bp)
try:
 bp=u.load_asset(base);z=u.load_asset(car);c=u.get_default_object(E.load_blueprint_class(car));m=c.get_component_by_class(u.ChaosWheeledVehicleMovementComponent)
 scalar={p:m.get_editor_property(p) for p in ['mass','drag_coefficient','chassis_width','chassis_height']};structs={p:m.get_editor_property(p).export_text() for p in ['engine_setup','transmission_setup','differential_setup']};wheels=[s.export_text() for s in m.get_editor_property('wheel_setups')]
 ss=u.get_engine_subsystem(u.SubobjectDataSubsystem);lib=u.SubobjectDataBlueprintFunctionLibrary
 for short in ['Idle','Run']:
  name='DieselFallback_'+short+'Loop';path='/Game/Zafira/Audio/'+name
  if not E.does_asset_exist(path):
   t=u.AssetImportTask();t.filename='D:/blender/project/zafira/driving/audio/processed/'+name+'.wav';t.destination_path='/Game/Zafira/Audio';t.destination_name=name;t.automated=True;t.save=True;t.replace_existing=False;u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
  sound=u.load_asset(path);assert sound;sound.set_editor_property('looping',True);sound.set_editor_property('virtualization_mode',u.VirtualizationMode.PLAY_WHEN_SILENT);E.save_loaded_asset(sound,False)
  hs=ss.k2_gather_subobject_data_for_blueprint(bp);name='ZafiraDiesel'+short
  objects={lib.get_object(lib.get_data(h)).get_name():h for h in hs}
  h=next((h for key,h in objects.items() if key.startswith(name)),None)
  if h is None:
   h,reason=ss.add_new_subobject(u.AddNewSubobjectParams(parent_handle=hs[0],new_class=u.AudioComponent,blueprint_context=bp));assert not str(reason),str(reason);ss.rename_subobject(h,name)
  obj=lib.get_object(lib.get_data(h));obj.set_editor_property('sound',sound);obj.set_editor_property('auto_activate',True);obj.set_editor_property('volume_multiplier',.5 if short=='Idle' else .03);obj.set_editor_property('pitch_multiplier',1.0);obj.set_editor_property('allow_spatialization',False)
 event=G.get_graph_editor_by_name(bp,'EventGraph')
 for name,value in [('ZafiraAudioRPM','850'),('ZafiraAudioLoad','0')]:
  if name not in L.list_member_variable_names(bp,False):assert event.add_member_variable(name,L.get_basic_type_by_name('real'),value)
 if 'ZafiraUpdateDieselAudio' in L.list_graph_names(bp):L.remove_function_graph(bp,'ZafiraUpdateDieselAudio')
 g=G.create_and_edit_function_graph(bp,'ZafiraUpdateDieselAudio');p=g.find_graph_entry_pin()
 dt=call(g,'GameplayStatics.GetWorldDeltaSeconds')
 for var,fn,owner,lo,hi,speed in [('ZafiraAudioRPM','GetEngineRotationSpeed','ChaosWheeledVehicleMovementComponent',850,4800,5),('ZafiraAudioLoad','GetThrottleInput','ChaosVehicleMovementComponent',0,1,7)]:
  n=call(g,'/Script/ChaosVehicles.'+owner+'.'+fn);link(get(g,'Chaos Wheeled Vehicle Movement Component'),n.find_self_pin());p=chain(p,n) if n.find_execute_pin().is_valid() else p;clamp=math(g,'FClamp',Min=lo,Max=hi);link(result(n),clamp.find_input_pin('Value'));interp=math(g,'FInterpTo',InterpSpeed=speed);link(get(g,var),interp.find_input_pin('Current'));link(result(clamp),interp.find_input_pin('Target'));link(result(dt),interp.find_input_pin('DeltaTime'));st=g.add_set_member_variable_node(var);link(result(interp),st.find_input_pin(var));p=chain(p,st)
 def mapped(var,a,b,c,d):
  n=math(g,'MapRangeClamped',InRangeA=a,InRangeB=b,OutRangeA=c,OutRangeB=d);link(get(g,var),n.find_input_pin('Value'));return result(n)
 for short,a,b,v0,v1 in [('Idle',.85,1.65,.65,.06),('Run',.75,2.5,.03,.62)]:
  pitch=mapped('ZafiraAudioRPM',850,4800,a,b);volume=mapped('ZafiraAudioRPM',850,3000,v0,v1);load=mapped('ZafiraAudioLoad',0,1,.7,1.15);mul=math(g,'Multiply_DoubleDouble');link(volume,mul.find_input_pin('A'));link(load,mul.find_input_pin('B'))
  for fn,key,value in [('SetPitchMultiplier','NewPitchMultiplier',pitch),('SetVolumeMultiplier','NewVolumeMultiplier',result(mul))]:
   n=call(g,'AudioComponent.'+fn);link(get(g,'ZafiraDiesel'+short),n.find_self_pin());link(value,n.find_input_pin(key));p=chain(p,n)
 compiled();event=G.get_graph_editor_by_name(bp,'EventGraph');anchor=next(n for n in event.list_all_nodes() if n.get_node_title()=='ZafiraTransmissionInput');anchor.find_then_pin().break_pin_links();n=call(event,base+'.BP_VehicleAdvPawnBase_C:ZafiraUpdateDieselAudio');chain(anchor.find_then_pin(),n)
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
 r.update(success=True,status='saved',errors=errors,scalar_preserved=scalar,structs_preserved=structs,wheel_setups=wheels,graphs=[str(n) for n in L.list_graph_names(bp)],implementation='Two autoactivated looping AudioComponents; native Blueprint tick smoothed actual Chaos RPM/throttle pitch and crossfade. No startup replay, no runtime Python.')
except:r['error']=traceback.format_exc();u.log_error(r['error'])
finally:(S/'audio_build_report.json').write_text(json.dumps(r,indent=2))
assert r.get('success'),r
