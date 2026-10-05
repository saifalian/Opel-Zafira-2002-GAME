import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
def key(name):
    k=u.Key(); k.set_editor_property('key_name', u.Name(name)); return k
try:
    tex_path='/Game/VehicleTemplate/Input/TouchControlsV2/T_'
    tex={n:u.load_asset(tex_path+n) for n in ['AUTOONLY','CAMERA','FORWARD','BRAKE','HANDBRAKE','LEFT','RIGHT']}
    def ctrl(name, center, size, interact, main_key, scale=(1,1), alt_key=None):
        c=u.TouchInputControl(); c.set_editor_property('treat_as_button', True)
        c.set_editor_property('image1', tex[name]); c.set_editor_property('image2', tex[name])
        c.set_editor_property('center', u.Vector2D(*center))
        c.set_editor_property('visual_size', u.Vector2D(*size))
        c.set_editor_property('thumb_size', u.Vector2D(0,0))
        c.set_editor_property('interaction_size', u.Vector2D(*interact))
        c.set_editor_property('input_scale', u.Vector2D(*scale))
        c.set_editor_property('main_input_key', key(main_key))
        if alt_key: c.set_editor_property('alt_input_key', key(alt_key))
        return c
    ti=u.load_asset('/Game/VehicleTemplate/Input/TI_ZafiraRequestedMobile'); ti.modify()
    controls=[
        ctrl('AUTOONLY',(0.075,0.075),(0.105,0.105),(0.12,0.12),'F10'),
        ctrl('CAMERA',(0.930,0.080),(0.085,0.085),(0.10,0.10),'C'),
        ctrl('FORWARD',(0.865,0.300),(0.090,0.090),(0.11,0.11),'Gamepad_RightTriggerAxis'),
        ctrl('BRAKE',(0.915,0.430),(0.090,0.090),(0.11,0.11),'Gamepad_LeftTriggerAxis'),
        ctrl('HANDBRAKE',(0.920,0.570),(0.090,0.090),(0.11,0.11),'Gamepad_FaceButton_Bottom'),
        ctrl('LEFT',(0.745,0.875),(0.090,0.090),(0.11,0.11),'Gamepad_LeftX',(-1,1)),
        ctrl('RIGHT',(0.900,0.830),(0.090,0.090),(0.11,0.11),'Gamepad_LeftX',(1,1)),
    ]
    ti.set_editor_property('controls',controls)
    ti.set_editor_property('active_opacity',0.88); ti.set_editor_property('inactive_opacity',0.72)
    ti.set_editor_property('time_until_deactive',999.0); ti.set_editor_property('time_until_reset',0.05); ti.set_editor_property('startup_delay',0.0)
    u.EditorAssetLibrary.save_loaded_asset(ti,False)
    report={'success':True,'note':'old UMG widget disabled separately; controls now use gamepad axes so right/left have opposite steering signs','controls':[c.export_text() for c in controls]}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(P/'Scripts/touch_controls_gamepad_axes_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))