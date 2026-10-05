import unreal as u,json,pathlib
c=u.TouchInputControl()
r={'default':c.to_dict(), 'text':c.export_text()}
t=u.TouchInterface()
r['ti_props']={k: str(t.get_editor_property(k)) for k in ['controls','active_opacity','inactive_opacity','time_until_deactive','time_until_reset','activation_delay','startup_delay'] if True}
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/touch_struct.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))