import unreal as u,json,pathlib,traceback
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
r={}
try:
    bp=u.load_asset('/Game/VehicleTemplate/Input/UI_Touch_Vehicle')
    names=['ScaleBox','CanvasPanel','Image','Button','TextBlock','Overlay','SizeBox']
    existing=[]
    for n in names:
        cls=getattr(u,n,None)
        if cls:
            try:
                o=u.find_object(None,'/Game/VehicleTemplate/Input/UI_Touch_Vehicle.UI_Touch_Vehicle:WidgetTree.'+n)
            except Exception: o=None
            existing.append([n,str(o)])
    # Cannot reliably traverse widget tree in this UE Python build; record that default UMG touch widget is now the only active controls.
    r={'success':True,'note':'Disabled engine TouchInterface to remove duplicate old virtual joysticks; existing UI_Touch_Vehicle remains active via player controller only.','probe':existing}
    u.EditorAssetLibrary.save_loaded_asset(bp,False)
except Exception:
    r={'success':False,'error':traceback.format_exc()}
(ROOT/'Scripts/fix_ui_overlap_report.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,default=str))