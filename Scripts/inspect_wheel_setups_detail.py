import unreal as u, pathlib, json, traceback
out={}
try:
  for bp_path in ['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase','/Game/Zafira/BP_Zafira']:
    bp=u.load_asset(bp_path); ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
    for h in ss.k2_gather_subobject_data_for_blueprint(bp):
      obj=lib.get_object(lib.get_data(h))
      if isinstance(obj,u.ChaosWheeledVehicleMovementComponent):
        arr=obj.get_editor_property('wheel_setups')
        rows=[]
        for i,w in enumerate(arr):
          rows.append({'i':i,'str':str(w),'dict':w.to_dict() if hasattr(w,'to_dict') else None,'dir':[x for x in dir(w) if not x.startswith('_')][:100]})
        out[bp_path]=rows
except Exception: out={'error':traceback.format_exc()}
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/wheel_setups_detail.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
