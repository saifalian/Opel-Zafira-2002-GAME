import unreal,json,os
ROOT='D:/unreal engine/project/ZafiraDrive'
E=unreal.EditorAssetLibrary
base='/Game/VehicleTemplate/Blueprints/'
# Duplicate the working template pawn, retaining all Blueprint input graphs and cameras.
bp=E.load_asset('/Game/Zafira/BP_Zafira') or E.duplicate_asset(base+'SportsCar/BP_VehicleAdvSportsCar','/Game/Zafira/BP_Zafira')
cls=E.load_blueprint_class('/Game/Zafira/BP_Zafira'); cdo=unreal.get_default_object(cls)
m=cdo.get_component_by_class(unreal.ChaosWheeledVehicleMovementComponent)
m.modify();m.set_editor_property('mass',1555.0)
e=m.get_editor_property('engine_setup')
e.set_editor_properties({'max_torque':280.,'max_rpm':4700.,'engine_idle_rpm':800.,'engine_brake_effect':0.12,'engine_rev_up_moi':1.0})
curve=unreal.RuntimeFloatCurve()
points=[(0,0.45),(800,0.55),(1200,0.8),(1500,1),(2750,1),(3500,.89),(4000,92000/(4000*2*3.141592653589793/60)/280),(4500,.62),(4700,0.3)]
curve.import_text('(EditorCurveData=(Keys=('+','.join('(InterpMode=RCIM_Linear,Time=%s,Value=%s)'%p for p in points)+')))')
e.set_editor_property('torque_curve',curve);m.set_editor_property('engine_setup',e)
t=m.get_editor_property('transmission_setup');t.set_editor_properties({'use_automatic_gears':True,'use_auto_reverse':True,'forward_gear_ratios':[3.67,1.88,1.18,.89,.66],'reverse_gear_ratios':[3.43],'final_ratio':3.818,'change_up_rpm':4200.,'change_down_rpm':1500.,'gear_change_time':.35,'transmission_efficiency':.9});m.set_editor_property('transmission_setup',t)
d=m.get_editor_property('differential_setup');d.set_editor_property('differential_type',unreal.VehicleDifferential.FRONT_WHEEL_DRIVE);m.set_editor_property('differential_setup',d)
wheels=[]
for axle in ['Front','Rear']:
 path='/Game/Zafira/BP_Wheels'+axle
 wb=E.load_asset(path) or E.duplicate_asset(base+'SportsCar/SportsCar_Wheels'+axle,path)
 wc=E.load_blueprint_class(path);wd=unreal.get_default_object(wc);wd.modify()
 wd.set_editor_properties({'affected_by_engine':axle=='Front','affected_by_brake':True,'affected_by_handbrake':axle=='Rear','max_steer_angle':35. if axle=='Front' else 0.,'wheel_radius':31.6,'wheel_width':20.5,'spring_rate':300.,'spring_preload':50.,'suspension_damping_ratio':.65,'suspension_max_raise':10.,'suspension_max_drop':12.,'friction_force_multiplier':2.0,'max_brake_torque':2000.})
 unreal.BlueprintEditorLibrary.compile_blueprint(wb);E.save_loaded_asset(wb,False);wheels.append(wc)
setups=m.get_editor_property('wheel_setups')
for i,s in enumerate(setups):
 bone=str(s.get_editor_property('bone_name'));s.set_editor_property('wheel_class',wheels[0 if '_F' in bone else 1]);s.set_editor_property('additional_offset',unreal.Vector(0,0,-7.4))
m.set_editor_property('wheel_setups',setups)
unreal.BlueprintEditorLibrary.compile_blueprint(bp);E.save_loaded_asset(bp,False)
gm=E.load_asset('/Game/Zafira/BP_ZafiraGameMode') or E.duplicate_asset(base+'BP_VehicleAdvGameMode','/Game/Zafira/BP_ZafiraGameMode')
gc=unreal.get_default_object(E.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode'));gc.set_editor_property('default_pawn_class',cls);unreal.BlueprintEditorLibrary.compile_blueprint(gm);E.save_loaded_asset(gm,False)
# A large flat physics test surface avoids template track barriers during telemetry.
world=unreal.EditorLoadingAndSavingUtils.new_blank_map(False)
a=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
floor=a.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(0,0,-50));floor.set_actor_label('Zafira_TestGround_4km');floor.static_mesh_component.set_static_mesh(E.load_asset('/Engine/BasicShapes/Cube'));floor.set_actor_scale3d(unreal.Vector(4000,2000,1))
floor.static_mesh_component.set_mobility(unreal.ComponentMobility.STATIC)
a.spawn_actor_from_class(unreal.PlayerStart,unreal.Vector(0,0,150))
sun=a.spawn_actor_from_class(unreal.DirectionalLight,unreal.Vector(0,0,1000),unreal.Rotator(-45,25,0));sun.light_component.set_editor_property('intensity',5.)
a.spawn_actor_from_class(unreal.SkyLight,unreal.Vector(0,0,500))
a.spawn_actor_from_class(unreal.SkyAtmosphere,unreal.Vector())
world.get_world_settings().set_editor_property('default_game_mode',E.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode'))
unreal.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraTest')
# Record the actual serialized struct text, not Python opaque wrappers.
m=unreal.get_default_object(E.load_blueprint_class('/Game/Zafira/BP_Zafira')).get_component_by_class(unreal.ChaosWheeledVehicleMovementComponent)
report={'mass':m.get_editor_property('mass'),'torque_points':points,'targets_unverified':{'top_kmh':187,'zero_to_100_seconds':11.5},'configs':{p:m.get_editor_property(p).export_text() for p in ['engine_setup','transmission_setup','differential_setup','steering_setup']}}
open(ROOT+'/Scripts/saved_tuning.json','w').write(json.dumps(report,indent=2))
print('ZAFIRA_BUILD_COMPLETE')
