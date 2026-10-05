import unreal as u,json,pathlib
v=u.DeprecateSlateVector2D(); r={'dir':[x for x in dir(v) if not x.startswith('_')], 'text': str(v)}
for p in ['x','y','X','Y']:
 try: v.set_editor_property(p,256); r[p]='ok'
 except Exception as e: r[p]=str(e)
r['after']=str(v)
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/slatevec.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))