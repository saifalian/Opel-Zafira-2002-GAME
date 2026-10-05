import unreal as u,json,pathlib
bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase')
ss=u.get_engine_subsystem(u.SubobjectDataSubsystem);lib=u.SubobjectDataBlueprintFunctionLibrary
arr=[]
for h in ss.k2_gather_subobject_data_for_blueprint(bp):
 o=lib.get_object(lib.get_data(h)); arr.append({'name':o.get_name(),'class':o.get_class().get_name()})
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/base_components.json').write_text(json.dumps(arr,indent=2))
print(json.dumps(arr,indent=2))