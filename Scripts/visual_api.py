import unreal as u,json,pathlib
r={}
for clsname in ['ExponentialHeightFog','PostProcessVolume','VolumetricCloud','SunSky','SkyLight','DirectionalLight','StaticMeshActor']:
    cls=getattr(u,clsname,None); r[clsname]=[x for x in dir(cls) if 'property' in x.lower() or 'component' in x.lower()][:50] if cls else None
for clsname in ['PostProcessSettings','SkyLightComponent','DirectionalLightComponent']:
    cls=getattr(u,clsname,None); r[clsname]=[x for x in dir(cls) if 'exposure' in x.lower() or 'intensity' in x.lower()][:80] if cls else None
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/visual_api.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))