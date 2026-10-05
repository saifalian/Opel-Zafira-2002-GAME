import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
def key(name):
    k=u.Key(); k.set_editor_property('key_name', u.Name(name)); return k
try:
    tex_path='/Game/VehicleTemplate/Input/TouchControlsV2/T_'
    tex={n:u.load_asset(tex_path+n) for n in ['AUTOONLY','CAMERA','FORWARD','BRAKE','HANDBRAKE','LEFT','RIGHT']}
    def ctrl(name, center, size, interact, main_key, alt_key=None):
        c=u.TouchInputControl(); c.set_editor_property('treat_as_button', True)
        c.set_editor_property('image1', tex[name]); c.set_editor_property('image2', tex[name])
        c.set_editor_property('center', u.Vector2D(*center))
        c.set_editor_property('visual_size', u.Vector2D(*size))
        c.set_editor_property('thumb_size', u.Vector2D(0.02,0.02))
        c.set_editor_property('interaction_size', u.Vector2D(*interact))
        c.set_editor_property('input_scale', u.Vector2D(1,1))
        c.set_editor_property('main_input_key', key(main_key))
        if alt_key: c.set_editor_property('alt_input_key', key(alt_key))
        return c
    ti=u.load_asset('/Game/VehicleTemplate/Input/TI_ZafiraRequestedMobile'); ti.modify()
    controls=[
        ctrl('AUTOONLY',(0.075,0.075),(0.105,0.105),(0.14,0.14),'F10'),
        ctrl('CAMERA',(0.910,0.075),(0.100,0.100),(0.13,0.13),'C','Tab'),
        ctrl('FORWARD',(0.900,0.260),(0.105,0.105),(0.14,0.14),'W','Up'),
        ctrl('BRAKE',(0.900,0.420),(0.105,0.105),(0.14,0.14),'S','Down'),
        ctrl('HANDBRAKE',(0.900,0.590),(0.105,0.105),(0.14,0.14),'SpaceBar'),
        ctrl('LEFT',(0.720,0.875),(0.105,0.105),(0.14,0.14),'A','Left'),
        ctrl('RIGHT',(0.900,0.875),(0.105,0.105),(0.14,0.14),'D','Right'),
    ]
    ti.set_editor_property('controls',controls)
    ti.set_editor_property('active_opacity',0.80); ti.set_editor_property('inactive_opacity',0.65)
    u.EditorAssetLibrary.save_loaded_asset(ti,False)
    report={'success':True,'note':'resized mobile controls to normalized 10.5% screen width so they do not cover gameplay','controls':[c.export_text() for c in controls]}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(P/'Scripts/resize_mobile_controls_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
