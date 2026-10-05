import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
r={}
try:
    for bp_path in ['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase','/Game/Zafira/BP_Zafira']:
        bp=E.load_asset(bp_path); ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
        vals=[]
        for h in ss.k2_gather_subobject_data_for_blueprint(bp):
            o=lib.get_object(lib.get_data(h))
            if isinstance(o,u.ChaosWheeledVehicleMovementComponent):
                o.modify()
                for call,args in [('set_use_automatic_gears',[True]),('set_target_gear',[1,True]),('set_requires_controller_for_inputs',[False]),('set_affected_by_engine',[0,True]),('set_affected_by_engine',[1,True]),('set_affected_by_engine',[2,True]),('set_affected_by_engine',[3,True])]:
                    try:
                        getattr(o,call)(*args); vals.append(call+str(args)+' ok')
                    except Exception as e: vals.append(call+str(args)+' ERR '+str(e))
                try: vals.append('auto='+str(o.get_use_auto_gears())+' target='+str(o.get_target_gear()))
                except Exception as e: vals.append('read ERR '+str(e))
        L.compile_blueprint(bp); E.save_loaded_asset(bp,False); r[bp_path]=vals
except Exception:
    r={'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'force_vehicle_auto_methods_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
