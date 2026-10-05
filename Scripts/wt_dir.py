import unreal as u,json,pathlib
wt=u.find_object(None,'/Game/VehicleTemplate/Input/UI_Touch_Vehicle.UI_Touch_Vehicle:WidgetTree')
r={'dir':[x for x in dir(wt) if not x.startswith('_')] if wt else None}
for m in (r['dir'] or []):
 if any(s in m.lower() for s in ['widget','child','root','find','all']):
  try: r[m]=str(getattr(wt,m))
  except: pass
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/wt_dir.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))