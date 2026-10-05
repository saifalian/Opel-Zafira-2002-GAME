import unreal as u,json,pathlib
k=u.Key(); r={'key_dir':[x for x in dir(k) if not x.startswith('_')], 'text':k.export_text()}
for p in ['key_name','KeyName','name']:
 try: k.set_editor_property(p,'Gamepad_LeftX'); r[p]='ok '+k.export_text()
 except Exception as e: r[p]=str(e)
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/key_api.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))