import unreal as u, inspect, pathlib
out=[]
for fn in ['new_map_from_template','save_map']:
    f=getattr(u.EditorLoadingAndSavingUtils,fn)
    out.append(fn+': '+str(f))
    out.append(str(f.__doc__))
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/save_doc.txt'); path.write_text('\n'.join(out)); print(path)
