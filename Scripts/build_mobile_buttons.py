import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
SRC=P/'SourceArt/TouchButtons'
DEST='/Game/VehicleTemplate/Input/TouchLabels'
report={'imported':[]}
try:
    tools=u.AssetToolsHelpers.get_asset_tools()
    tasks=[]
    for png in SRC.glob('*.png'):
        t=u.AssetImportTask(); t.filename=str(png); t.destination_path=DEST; t.destination_name='T_Button_'+png.stem; t.automated=True; t.save=True; t.replace_existing=True; tasks.append(t)
    tools.import_asset_tasks(tasks)
    tex={}
    for png in SRC.glob('*.png'):
        path=f'{DEST}/T_Button_{png.stem}'
        obj=u.EditorAssetLibrary.load_asset(path)
        tex[png.stem]=obj; report['imported'].append(path)
        if obj: u.EditorAssetLibrary.save_asset(path)
    def brush(texture):
        v=u.DeprecateSlateVector2D(); v.set_editor_property('x',256); v.set_editor_property('y',256); b=u.SlateBrush(); b.set_editor_property('resource_object', texture); b.set_editor_property('image_size', v); return b
    def ctrl(name, center, visual, interact, main, alt=None, button=True, scale=(1,1)):
        c=u.TouchInputControl();
        c.set_editor_property('treat_as_button', button)
        c.set_editor_property('image1', tex[name]); c.set_editor_property('image2', tex[name])
        c.set_editor_property('center', u.Vector2D(*center)); c.set_editor_property('visual_size', u.Vector2D(*visual)); c.set_editor_property('thumb_size', u.Vector2D(72,72)); c.set_editor_property('interaction_size', u.Vector2D(*interact))
        c.set_editor_property('input_scale', u.Vector2D(*scale)); k=u.Key(); k.set_editor_property('key_name', main); c.set_editor_property('main_input_key', k)
        if alt:
            k2=u.Key(); k2.set_editor_property('key_name', alt); c.set_editor_property('alt_input_key', k2)
        return c
    asset_path='/Game/VehicleTemplate/Input/TI_ZafiraMobile'
    if u.EditorAssetLibrary.does_asset_exist(asset_path): ti=u.EditorAssetLibrary.load_asset(asset_path)
    else: ti=tools.create_asset('TI_ZafiraMobile','/Game/VehicleTemplate/Input',u.TouchInterface,u.TouchInterfaceFactory())
    controls=[
      ctrl('STEER',(0.16,0.76),(180,180),(260,260),'Gamepad_LeftX','Gamepad_LeftY',False,(1,-1)),
      ctrl('GAS',(0.86,0.58),(145,145),(180,180),'Gamepad_RightTriggerAxis',None,True),
      ctrl('BRAKE',(0.86,0.80),(145,145),(180,180),'Gamepad_LeftTriggerAxis',None,True),
      ctrl('HAND',(0.68,0.80),(120,120),(150,150),'Gamepad_RightShoulder',None,True),
      ctrl('CAMERA',(0.70,0.58),(110,110),(140,140),'Gamepad_LeftShoulder',None,True),
      ctrl('RESET',(0.53,0.80),(105,105),(135,135),'Gamepad_Special_Right',None,True),
      ctrl('LOOK',(0.53,0.58),(105,105),(150,150),'Gamepad_RightX','Gamepad_RightY',False,(1,-1)),
    ]
    ti.modify(); ti.set_editor_property('controls', controls); ti.set_editor_property('active_opacity', 0.85); ti.set_editor_property('inactive_opacity',0.65); ti.set_editor_property('time_until_deactive', 4.0); ti.set_editor_property('time_until_reset', 0.2); ti.set_editor_property('startup_delay',0.0)
    u.EditorAssetLibrary.save_loaded_asset(ti, False); report['touch_interface']=asset_path; report['controls']=[c.export_text() for c in controls]
    # Make HUD instruction text larger/clearer on UI_Vehicle where possible.
    hud=u.load_asset('/Game/VehicleTemplate/UI/UI_Vehicle')
    for name,text,size in [('UnitLabel','LEFT = STEER   RIGHT: GAS / BRAKE   CAM / RESET / HANDBRAKE',20),('GearLabel','AUTO',24)]:
        o=u.find_object(None,f'/Game/VehicleTemplate/UI/UI_Vehicle.UI_Vehicle:WidgetTree.{name}')
        if o:
            o.modify();
            try: o.set_text(u.Text.cast(text))
            except Exception: pass
            try:
                f=o.get_editor_property('font'); f.set_editor_property('size',size); o.set_editor_property('font',f)
            except Exception: pass
    u.EditorAssetLibrary.save_loaded_asset(hud, False)
    report['success']=True
except Exception:
    report['success']=False; report['error']=traceback.format_exc(); u.log_error(report['error'])
(P/'Scripts/mobile_buttons_report.json').write_text(json.dumps(report,indent=2,default=str))
assert report.get('success'), report