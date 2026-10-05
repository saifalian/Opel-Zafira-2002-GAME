import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
def key(name):
    k=u.Key(); k.set_editor_property('key_name', u.Name(name)); return k
try:
    tex_path='/Game/VehicleTemplate/Input/TouchControlsV2/T_'
    tex={n:u.load_asset(tex_path+n) for n in ['AUTOONLY','CAMERA','FORWARD','BRAKE','HANDBRAKE','LEFT','RIGHT']}
    # Use an existing transparent-ish/neutral texture if no dedicated invisible texture exists.
    look_tex=tex.get('CAMERA')
    def button(name, center, kname, alt=None):
        c=u.TouchInputControl(); c.set_editor_property('treat_as_button', True)
        c.set_editor_property('image1', tex[name]); c.set_editor_property('image2', tex[name])
        c.set_editor_property('center', u.Vector2D(*center))
        c.set_editor_property('visual_size', u.Vector2D(0.105,0.105))
        c.set_editor_property('thumb_size', u.Vector2D(0.0,0.0))
        c.set_editor_property('interaction_size', u.Vector2D(0.108,0.108))
        c.set_editor_property('input_scale', u.Vector2D(1.0,1.0))
        c.set_editor_property('main_input_key', key(kname))
        if alt: c.set_editor_property('alt_input_key', key(alt))
        return c
    def look_zone():
        c=u.TouchInputControl(); c.set_editor_property('treat_as_button', False)
        c.set_editor_property('image1', look_tex); c.set_editor_property('image2', look_tex)
        c.set_editor_property('center', u.Vector2D(0.50,0.42))
        # Visual is almost zero: the swipe zone is functional but not a draggable visible joystick.
        c.set_editor_property('visual_size', u.Vector2D(0.001,0.001))
        c.set_editor_property('thumb_size', u.Vector2D(0.0,0.0))
        c.set_editor_property('interaction_size', u.Vector2D(0.46,0.48))
        c.set_editor_property('input_scale', u.Vector2D(1.4,-1.0))
        c.set_editor_property('main_input_key', key('Gamepad_RightX'))
        c.set_editor_property('alt_input_key', key('Gamepad_RightY'))
        return c
    ti=u.load_asset('/Game/VehicleTemplate/Input/TI_ZafiraRequestedMobile'); ti.modify()
    controls=[
        button('AUTOONLY',(0.075,0.075),'F10'),
        button('CAMERA',(0.930,0.075),'C','Tab'),
        button('FORWARD',(0.095,0.360),'W','Up'),
        button('BRAKE',(0.095,0.520),'S','Down'),
        button('HANDBRAKE',(0.095,0.680),'SpaceBar'),
        button('LEFT',(0.795,0.760),'A','Left'),
        button('RIGHT',(0.925,0.760),'D','Right'),
        look_zone(),
    ]
    ti.set_editor_property('controls',controls)
    ti.set_editor_property('active_opacity',0.90); ti.set_editor_property('inactive_opacity',0.80)
    ti.set_editor_property('time_until_deactive',999.0); ti.set_editor_property('time_until_reset',0.0); ti.set_editor_property('startup_delay',0.0)
    u.EditorAssetLibrary.save_loaded_asset(ti,False)
    # Add gamepad right stick look mappings where the controller already listens.
    action=u.load_asset('/Game/VehicleTemplate/Input/Actions/IA_LookAround')
    updated=[]
    for ctx_path in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/VehicleTemplate/Input/IMC_Vehicle_MouseLook','/Game/VehicleTemplate/Input/IMC_SteeringWheel']:
        ctx=u.load_asset(ctx_path)
        if not (ctx and action): continue
        ctx.modify()
        for kn in ['Gamepad_RightX','Gamepad_RightY','MouseX','MouseY']:
            try: ctx.map_key(action, key(kn))
            except Exception as e: updated.append([ctx_path,kn,'err',str(e)])
        u.EditorAssetLibrary.save_loaded_asset(ctx,False)
        updated.append([ctx_path,'saved'])
    # Keep old UMG touch widget off.
    bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
    if bp:
        gen=bp.generated_class() if callable(bp.generated_class) else bp.generated_class
        cdo=u.get_default_object(gen)
        try: cdo.set_editor_property('Touch Controls Widget Class', None)
        except Exception as e: report['old_widget_disable_error']=str(e)
        u.EditorAssetLibrary.save_loaded_asset(bp,False)
    report.update({'success':True,'note':'added invisible center swipe look zone using Gamepad_RightX/Y; fixed buttons remain left/right and non-drag visible','updated_mappings':updated,'controls':[c.export_text() for c in controls]})
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(P/'Scripts/add_mobile_swipe_camera_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))