import unreal as u, pathlib, json
out={}
for method in ['set_editor','attr','ctor']:
    try:
        if method=='set_editor':
            k=u.Key(); k.set_editor_property('key_name', u.Name('W'))
        elif method=='attr':
            k=u.Key(); k.key_name='W'
        else:
            k=u.Key('W')
        out[method]={'str':str(k),'dict':k.to_dict(),'tuple':str(k.to_tuple()),'export':k.export_text()}
    except Exception as e: out[method]='ERR '+str(e)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/key_creation_test.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
