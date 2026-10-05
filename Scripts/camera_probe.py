import unreal as u,json,pathlib,traceback
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts');r={}
try:
 for path in ['/Game/Zafira/BP_Zafira','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController']:
  b=u.load_asset(path);z={'graphs':{},'vars':list(u.BlueprintEditorLibrary.list_member_variable_names(b))};r[path]=z
  for name in u.BlueprintEditorLibrary.list_graph_names(b):
   g=u.BlueprintGraphEditor.get_graph_editor_by_name(b,name);ns=[];z['graphs'][str(name)]=ns
   for n in g.list_all_nodes():
    ns.append({'name':n.get_name(),'title':n.get_node_title(),'class':n.get_class().get_name(),'pins':[{'name':str(p.get_pin_name()),'dir':str(p.get_pin_direction()),'value':p.get_pin_value(),'links':[q.get_owning_node().get_name()+':'+str(q.get_pin_name()) for q in p.list_connected_pins()]} for p in n.list_all_pins()]})
  if path.endswith('BP_Zafira'):
   s=u.get_engine_subsystem(u.SubobjectDataSubsystem);l=u.SubobjectDataBlueprintFunctionLibrary;z['components']=[]
   for h in s.k2_gather_subobject_data_for_blueprint(b):
    o=l.get_object(l.get_data(h));d={'name':o.get_name(),'class':o.get_class().get_name()}
    for p in ['relative_location','relative_rotation','target_arm_length','use_pawn_control_rotation','inherit_pitch','inherit_yaw','inherit_roll','auto_activate','field_of_view']:
     try:d[p]=str(o.get_editor_property(p))
     except:pass
    z['components'].append(d)
 for p in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/VehicleTemplate/Input/IMC_Vehicle_MouseLook']:
  r[p]=[m.export_text() for m in u.load_asset(p).get_editor_property('default_key_mappings').get_editor_property('mappings')]
except:r['error']=traceback.format_exc()
(R/'camera_probe.json').write_text(json.dumps(r,indent=2))
