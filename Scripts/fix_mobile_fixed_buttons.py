import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
def key(name):
    k=u.Key(); k.set_editor_property('key_name', u.Name(name)); return k
try:
    tex_path='/Game/VehicleTemplate/Input/TouchControlsV2/T_'
    tex={n:u.load_asset(tex_path+n) for n in ['AUTOONLY','CAMERA','FORWARD','BRAKE','HANDBRAKE','LEFT','RIGHT']}
    def ctrl(name, center, kname, alt=None):
        c=u.TouchInputControl()
        c.set_editor_property('treat_as_button', True)
        c.set_editor_property('image1', tex[name])
        c.set_editor_property('image2', tex[name])
        c.set_editor_property('center', u.Vector2D(*center))
        # normalized sizes: fixed-looking small buttons, no thumb/drag joystick
        c.set_editor_property('visual_size', u.Vector2D(0.105,0.105))
        c.set_editor_property('thumb_size', u.Vector2D(0.0,0.0))
        c.set_editor_property('interaction_size', u.Vector2D(0.108,0.108))
        c.set_editor_property('input_scale', u.Vector2D(1.0,1.0))
        c.set_editor_property('main_input_key', key(kname))
        if alt: c.set_editor_property('alt_input_key', key(alt))
        return c
    ti=u.load_asset('/Game/VehicleTemplate/Input/TI_ZafiraRequestedMobile')
    ti.modify()
    # User requested: throttle/brake/reverse on LEFT, steering LEFT/RIGHT on RIGHT.
    controls=[
        ctrl('AUTOONLY',(0.075,0.075),'F10'),       # manual unavailable / not in process
        ctrl('CAMERA',(0.930,0.075),'C','Tab'),
        ctrl('FORWARD',(0.095,0.360),'W','Up'),
        ctrl('BRAKE',(0.095,0.520),'S','Down'),
        ctrl('HANDBRAKE',(0.095,0.680),'SpaceBar'),
        ctrl('LEFT',(0.795,0.760),'A','Left'),
        ctrl('RIGHT',(0.925,0.760),'D','Right'),
    ]
    ti.set_editor_property('controls', controls)
    ti.set_editor_property('active_opacity', 0.92)
    ti.set_editor_property('inactive_opacity', 0.82)
    ti.set_editor_property('time_until_deactive', 999.0)
    ti.set_editor_property('time_until_reset', 0.0)
    ti.set_editor_property('startup_delay', 0.0)
    u.EditorAssetLibrary.save_loaded_asset(ti, False)
    # Keep old UMG touch widget disabled so only these controls show.
    bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
    if bp:
        gen=bp.generated_class() if callable(bp.generated_class) else bp.generated_class
        cdo=u.get_default_object(gen)
        try: cdo.set_editor_property('Touch Controls Widget Class', None)
        except Exception as e: report['disable_old_widget_error']=str(e)
        u.EditorAssetLibrary.save_loaded_asset(bp, False)
    report.update({'success':True,'note':'fixed non-drag button layout: gas/brake/handbrake left, steering right; keyboard keys used instead of virtual stick axis','controls':[c.export_text() for c in controls]})
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(P/'Scripts/fix_mobile_fixed_buttons_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))