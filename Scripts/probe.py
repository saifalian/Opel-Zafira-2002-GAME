import unreal,json
out={}
for n in ['VehicleEngineConfig','VehicleTransmissionConfig','VehicleDifferentialConfig','VehicleSteeringConfig','RuntimeFloatCurve','CurveFloat','SubobjectDataSubsystem','SubobjectDataBlueprintFunctionLibrary']:
 out[n]=str(getattr(unreal,n).__doc__)+'\n'+str(dir(getattr(unreal,n)))
w=unreal.EditorLoadingAndSavingUtils.load_map('/Game/VehicleTemplate/Maps/Lvl_VehicleBasic')
c=unreal.EditorAssetLibrary.load_blueprint_class('/Game/VehicleTemplate/Blueprints/SportsCar/BP_VehicleAdvSportsCar')
a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).spawn_actor_from_class(c,unreal.Vector(0,0,200))
out['spawncomponents']=[]
for comp in a.get_components_by_class(unreal.ActorComponent):
 d={'name':comp.get_name(),'class':comp.get_class().get_name()}
 if isinstance(comp,unreal.SkeletalMeshComponent):
  d['mesh']=str(comp.skeletal_mesh_asset);d['anim']=str(comp.anim_class);d['bones']=[{'name':str(comp.get_bone_name(i)),'transform':str(comp.get_socket_transform(comp.get_bone_name(i),unreal.RelativeTransformSpace.RTS_COMPONENT))} for i in range(comp.get_num_bones())]
 if isinstance(comp,unreal.ChaosWheeledVehicleMovementComponent):
  for prop in ['engine_setup','transmission_setup','differential_setup','steering_setup']:
   v=comp.get_editor_property(prop);d[prop]={x:str(getattr(v,x)) for x in dir(v) if not x.startswith('_') and not callable(getattr(v,x))}
  d['wheels']=[{p:str(x.get_editor_property(p)) for p in ['bone_name','wheel_class','additional_offset']} for x in comp.get_editor_property('wheel_setups')]
 out['spawncomponents'].append(d)
open('D:/unreal engine/project/ZafiraDrive/Scripts/probe.json','w').write(json.dumps(out,indent=2))
print('PROBE_COMPLETE')
