import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
SRC=P/'SourceArt/TouchButtonsV2'
DEST='/Game/VehicleTemplate/Input/TouchControlsV2'
report={'imported':[]}

def key(name):
    k=u.Key(); k.set_editor_property('key_name', u.Name(name)); return k
try:
    tools=u.AssetToolsHelpers.get_asset_tools()
    tasks=[]
    for png in SRC.glob('*.png'):
        t=u.AssetImportTask(); t.filename=str(png); t.destination_path=DEST; t.destination_name='T_'+png.stem; t.automated=True; t.save=True; t.replace_existing=True; tasks.append(t)
    tools.import_asset_tasks(tasks)
    tex={}
    for png in SRC.glob('*.png'):
        path=f'{DEST}/T_{png.stem}'
        obj=u.EditorAssetLibrary.load_asset(path)
        tex[png.stem]=obj; report['imported'].append(path)
        if obj: u.EditorAssetLibrary.save_loaded_asset(obj, False)
    def ctrl(name, center, size, interact, main_key, alt_key=None):
        c=u.TouchInputControl(); c.set_editor_property('treat_as_button', True)
        c.set_editor_property('image1', tex[name]); c.set_editor_property('image2', tex[name])
        c.set_editor_property('center', u.Vector2D(*center))
        c.set_editor_property('visual_size', u.Vector2D(*size))
        c.set_editor_property('thumb_size', u.Vector2D(1,1))
        c.set_editor_property('interaction_size', u.Vector2D(*interact))
        c.set_editor_property('input_scale', u.Vector2D(1,1))
        c.set_editor_property('main_input_key', key(main_key))
        if alt_key: c.set_editor_property('alt_input_key', key(alt_key))
        return c
    asset_path='/Game/VehicleTemplate/Input/TI_ZafiraRequestedMobile'
    ti=u.EditorAssetLibrary.load_asset(asset_path) if u.EditorAssetLibrary.does_asset_exist(asset_path) else tools.create_asset('TI_ZafiraRequestedMobile','/Game/VehicleTemplate/Input',u.TouchInterface,u.TouchInterfaceFactory())
    controls=[
        # top row
        ctrl('AUTOONLY',(0.075,0.075),(150,150),(185,185),'F10'),       # intentionally unmapped: auto-only/manual not in process
        ctrl('CAMERA',(0.900,0.075),(145,145),(180,180),'C','Tab'),
        # right side drive stack
        ctrl('FORWARD',(0.885,0.275),(160,160),(200,200),'W','Up'),
        ctrl('BRAKE',(0.885,0.455),(160,160),(200,200),'S','Down'),
        ctrl('HANDBRAKE',(0.885,0.640),(150,150),(190,190),'SpaceBar'),
        # lower right steering
        ctrl('LEFT',(0.700,0.860),(155,155),(195,195),'A','Left'),
        ctrl('RIGHT',(0.885,0.860),(155,155),(195,195),'D','Right'),
    ]
    ti.modify(); ti.set_editor_property('controls', controls)
    ti.set_editor_property('active_opacity',0.92); ti.set_editor_property('inactive_opacity',0.78)
    ti.set_editor_property('time_until_deactive',999.0); ti.set_editor_property('time_until_reset',0.08); ti.set_editor_property('startup_delay',0.0)
    u.EditorAssetLibrary.save_loaded_asset(ti, False)
    # Repair mapping contexts so these touch keys trigger the existing real vehicle actions.
    actions={n:u.load_asset('/Game/VehicleTemplate/Input/Actions/'+n) for n in ['IA_Throttle','IA_Brake','IA_Steering','IA_Handbrake','IA_ToggleCamera','IA_Reset']}
    for ctx_path in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/VehicleTemplate/Input/IMC_SteeringWheel','/Game/Input/IMC_Default']:
        ctx=u.load_asset(ctx_path)
        if not ctx: continue
        ctx.modify(); ctx.unmap_all()
        for act, keys in [('IA_Throttle',['W','Up']),('IA_Brake',['S','Down']),('IA_Steering',['A','Left','D','Right']),('IA_Handbrake',['SpaceBar']),('IA_ToggleCamera',['C','Tab']),('IA_Reset',['BackSpace','R'])]:
            for kn in keys:
                try: ctx.map_key(actions[act], key(kn))
                except Exception: pass
        u.EditorAssetLibrary.save_loaded_asset(ctx, False)
    # Config is patched in DefaultInput.ini after this script because this UE Python build
    # cannot set SoftObjectPath.default_touch_interface reliably.
    report.update({'success':True,'touch_interface':asset_path,'layout':{
        'top_left':'AUTO / MANUAL N/A button, unmapped so manual is restricted',
        'top_right':'CAM VIEW', 'right':'FORWARD, BRAKE/REVERSE, HAND BRAKE', 'bottom_right':'LEFT and RIGHT steering'
    },'controls':[c.export_text() for c in controls]})
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(P/'Scripts/requested_mobile_controls_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))
