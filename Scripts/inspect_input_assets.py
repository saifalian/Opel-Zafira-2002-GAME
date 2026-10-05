import unreal as u, pathlib, json
paths=['/Game/VehicleTemplate/Input/Actions/IA_Throttle','/Game/VehicleTemplate/Input/Actions/IA_Brake','/Game/VehicleTemplate/Input/Actions/IA_Steering','/Game/VehicleTemplate/Input/IMC_Vehicle_Default']
out={}
for p in paths:
    a=u.load_asset(p); d={'class':a.get_class().get_name() if a else None}
    if a:
        for prop in ['value_type','accumulation_behavior','trigger_events_that_consume_legacy_keys','default_key_mappings']:
            try: d[prop]=str(a.get_editor_property(prop))
            except Exception as e: pass
        if a.get_class().get_name()=='InputMappingContext':
            dk=a.get_editor_property('default_key_mappings')
            arr=dk.get_editor_property('mappings')
            d['mappings']=[]
            for m in arr:
                d['mappings'].append({'action':str(m.get_editor_property('action')),'key_export':m.get_editor_property('key').export_text(),'modifiers':str(m.get_editor_property('modifiers'))})
    out[p]=d
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/input_assets_report.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
