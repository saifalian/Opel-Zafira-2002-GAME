import unreal as u,json,pathlib
r={}
for clsname in ['TouchInterface','TouchInputControl']:
    cls=getattr(u,clsname,None); r[clsname]=[x for x in dir(cls) if not x.startswith('_')][:200] if cls else None
    if cls:
      try: r[clsname+'_props']=[p.get_name() for p in cls.static_class().get_properties()]
      except Exception as e: r[clsname+'_props_err']=str(e)
r['factory']=[x for x in dir(u) if 'Touch' in x or 'Texture2D' in x]
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/touch_api.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))