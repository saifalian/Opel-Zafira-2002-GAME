import unreal as u,json,pathlib,traceback
r={}
try:
 b=u.load_asset('/Game/VehicleTemplate/UI/UI_Vehicle')
 r['objects']=[]
 for name in ['UnitLabel','SpeedLabel','GearLabel']:
  o=u.find_object(None,'/Game/VehicleTemplate/UI/UI_Vehicle.UI_Vehicle:WidgetTree.'+name)
  r['objects'].append({'name':name,'object':str(o),'slot':str(o.get_editor_property('slot')) if o else ''})
 for n in ['create_node_from_name','add_get_member_variable_node','list_available_nodes','add_call_function_node']:r[n]=getattr(u.BlueprintGraphEditor,n).__doc__
 r['movement']=[x for x in dir(u.ChaosWheeledVehicleMovementComponent) if 'gear' in x or 'engine_rotation' in x]
except:r['error']=traceback.format_exc()
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/hud_api.json').write_text(json.dumps(r,indent=2,default=str))