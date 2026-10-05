import unreal as u, json, pathlib
r={}
for clsname in ['WidgetTree','WidgetBlueprint','WidgetBlueprintLibrary','WidgetBlueprintEditorLibrary','CanvasPanel','TextBlock','CanvasPanelSlot','Widget']:
    cls=getattr(u,clsname,None); r[clsname]=[x for x in dir(cls) if 'widget' in x.lower() or 'child' in x.lower() or 'slot' in x.lower() or 'create' in x.lower() or 'root' in x.lower()][:100] if cls else None
b=u.load_asset('/Game/VehicleTemplate/UI/UI_Vehicle')
r['bp_props']=[str(p) for p in b.get_class().get_properties()[:50]] if hasattr(b.get_class(),'get_properties') else 'no'
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/widget_api.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))