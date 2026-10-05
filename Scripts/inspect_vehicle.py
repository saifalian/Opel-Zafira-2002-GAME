import unreal, json
out={}
for name in ['BP_VehicleAdvPawnBase','SportsCar/BP_VehicleAdvSportsCar','OffroadCar/BP_VehicleAdvOffroadCar','BP_VehicleAdvGameMode']:
 c=unreal.EditorAssetLibrary.load_blueprint_class('/Game/VehicleTemplate/Blueprints/'+name)
 o=unreal.get_default_object(c)
 data={'class':str(c),'components':[]}
 for comp in o.get_components_by_class(unreal.ActorComponent):
  d={'name':comp.get_name(),'class':comp.get_class().get_name()}
  if isinstance(comp,unreal.ChaosWheeledVehicleMovementComponent):
   for p in ['mass','engine_setup','transmission_setup','differential_setup','wheel_setups','steering_setup']:
    d[p]=str(comp.get_editor_property(p))
   d['methods']=dir(comp)
  if isinstance(comp,unreal.SkeletalMeshComponent):
   d['mesh']=str(comp.get_editor_property('skeletal_mesh_asset')); d['anim']=str(comp.get_editor_property('anim_class'))
   d['bones']=[{'name':str(comp.get_bone_name(i)),'location':str(comp.get_socket_transform(comp.get_bone_name(i),unreal.RelativeTransformSpace.RTS_COMPONENT))} for i in range(comp.get_num_bones())]
  data['components'].append(d)
 if 'GameMode' in name: data['pawn']=str(o.get_editor_property('default_pawn_class'))
 out[name]=data
for n in ['SportsCar/SportsCar_WheelsFront','SportsCar/SportsCar_WheelsRear']:
 o=unreal.get_default_object(unreal.EditorAssetLibrary.load_blueprint_class('/Game/VehicleTemplate/Blueprints/'+n))
 out[n]={p:str(o.get_editor_property(p)) for p in ['wheel_radius','wheel_width','max_steer_angle','affected_by_engine','affected_by_brake','affected_by_handbrake','suspension_max_raise','suspension_max_drop','spring_rate','spring_preload','suspension_damping_ratio','friction_force_multiplier']}
open('D:/unreal engine/project/ZafiraDrive/Scripts/inspection.json','w').write(json.dumps(out,indent=2))
print('INSPECT_COMPLETE')
