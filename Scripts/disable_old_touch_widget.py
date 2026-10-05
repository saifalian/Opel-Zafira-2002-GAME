import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={}
try:
    bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
    gen=bp.generated_class() if callable(bp.generated_class) else bp.generated_class
    cdo=u.get_default_object(gen)
    attempts=[]
    for name in ['TouchControlsWidgetClass','touch_controls_widget_class','Touch Controls Widget Class','force_touch_controls','ForceTouchControls','use_mobile_controls','UseMobileControls']:
        try:
            before=cdo.get_editor_property(name)
            attempts.append([name,'get',str(before)])
        except Exception as e:
            attempts.append([name,'get_err',str(e)])
        try:
            if 'widget' in name.lower():
                cdo.set_editor_property(name, None)
            elif 'force' in name.lower() or 'mobile' in name.lower():
                cdo.set_editor_property(name, False)
            attempts.append([name,'set_ok',''])
        except Exception as e:
            attempts.append([name,'set_err',str(e)])
    u.EditorAssetLibrary.save_loaded_asset(bp, False)
    report={'success':True,'attempts':attempts}
except Exception:
    report={'success':False,'error':traceback.format_exc()}
(P/'Scripts/disable_old_touch_widget_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))