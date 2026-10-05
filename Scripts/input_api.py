import unreal as u,json,pathlib
r={}
for clsname in ['TouchInterface','InputSettings']:
 cls=getattr(u,clsname,None); r[clsname]=[x for x in dir(cls) if 'touch' in x.lower() or 'virtual' in x.lower() or 'default' in x.lower() or 'property' in x.lower()][:120] if cls else None
try:
 s=u.InputSettings.get_input_settings(); r['input_settings_props']={p:str(s.get_editor_property(p)) for p in ['always_show_touch_interface','default_touch_interface','use_mouse_for_touch']}
except Exception as e:r['input_settings_error']=str(e)
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/input_api.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))