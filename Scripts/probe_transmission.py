import unreal as u,json,pathlib,traceback
r={}
try:
 r['graph_methods']={x:getattr(u.BlueprintGraphEditor,x).__doc__ for x in dir(u.BlueprintGraphEditor) if any(y in x for y in ['input','node','variable'])}
 r['movement']={x:getattr(u.ChaosVehicleMovementComponent,x).__doc__ for x in ['set_use_automatic_gears','set_target_gear','get_use_auto_gears','get_current_gear'] if hasattr(u.ChaosVehicleMovementComponent,x)}
 b=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase');g=u.BlueprintGraphEditor.get_graph_editor_by_name(b,'EventGraph')
 r['nodes']=[{'name':n.get_name(),'title':n.get_node_title(),'pins':[{ 'name':str(p.get_pin_name()),'links':[q.get_owning_node().get_name()+':'+str(q.get_pin_name()) for q in p.list_connected_pins()]} for p in n.list_all_pins()]} for n in g.list_all_nodes() if 'CameraLook' in n.get_node_title() or n.get_name() in ['K2Node_CallFunction_23','K2Node_Event_0']]
 for path in ['/Script/Engine.PlayerController.WasInputKeyJustPressed','/Script/Engine.KismetSystemLibrary.PrintString','/Script/ChaosVehicles.ChaosVehicleMovementComponent.SetUseAutomaticGears']:
  n=g.add_call_function_node(path);r[path]=[str(p.get_pin_name()) for p in n.list_all_pins()] if n else None
except:r['error']=traceback.format_exc()
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/transmission_probe.json').write_text(json.dumps(r,indent=2))
