import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary
report={}
def key(name):
    k=u.Key(); k.set_editor_property('key_name', name); return k
def mod(cls, outer):
    return u.new_object(cls, outer=outer)
try:
    imc=E.load_asset('/Game/VehicleTemplate/Input/IMC_Vehicle_Default')
    assert imc, 'IMC missing'
    imc.modify(); imc.unmap_all()
    acts={n:E.load_asset('/Game/VehicleTemplate/Input/Actions/IA_'+n) for n in ['Throttle','Brake','Steering','Handbrake','Reset','ToggleCamera','LookAround']}
    made=[]
    def add(action_name,key_name,neg=False):
        a=acts[action_name]; assert a, action_name
        m=imc.map_key(a,key(key_name))
        if neg:
            m.set_editor_property('modifiers',[mod(u.InputModifierNegate, imc)])
        made.append({'action':action_name,'key':key_name,'neg':neg})
        return m
    # PC keyboard controls
    add('Throttle','W'); add('Throttle','Up'); add('Throttle','Gamepad_RightTriggerAxis')
    add('Brake','S'); add('Brake','Down'); add('Brake','Gamepad_LeftTriggerAxis')
    add('Steering','A',True); add('Steering','Left',True); add('Steering','Gamepad_LeftX')
    add('Steering','D'); add('Steering','Right')
    add('Handbrake','SpaceBar'); add('Handbrake','Gamepad_FaceButton_Bottom')
    add('Reset','R'); add('ToggleCamera','C'); add('ToggleCamera','Gamepad_Special_Left')
    E.save_loaded_asset(imc,False)
    # also ensure controller/GM use this mapping context by leaving default vehicle controller
    report={'success':True,'mapped':made,'count':len(made)}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'fix_vehicle_input_mappings_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')