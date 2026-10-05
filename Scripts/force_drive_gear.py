import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
r={}
try:
    for bp_path in ['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase','/Game/Zafira/BP_Zafira']:
        bp=E.load_asset(bp_path); cls=E.load_blueprint_class(bp_path); cdo=u.get_default_object(cls); cdo.modify()
        vals={}
        for p,v in [('ZafiraManualTransmission',False),('ZafiraRequestedGear',1)]:
            try:
                before=str(cdo.get_editor_property(p)); cdo.set_editor_property(p,v); after=str(cdo.get_editor_property(p)); vals[p]=[before,after]
            except Exception as e: vals[p]='ERR '+str(e)
        # configure vehicle movement transmission automatic where possible
        try:
            vm=cdo.get_editor_property('VehicleMovementComponent')
        except Exception:
            try: vm=cdo.get_editor_property('vehicle_movement_component')
            except Exception: vm=None
        if vm:
            for p,v in [('use_automatic_gears',True),('reverse_as_brake',True)]:
                try:
                    before=str(vm.get_editor_property(p)); vm.set_editor_property(p,v); vals['vm.'+p]=[before,str(vm.get_editor_property(p))]
                except Exception as e: vals['vm.'+p]='ERR '+str(e)
        L.compile_blueprint(bp); E.save_loaded_asset(bp,False); r[bp_path]=vals
except Exception:
    r={'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'force_drive_gear_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
