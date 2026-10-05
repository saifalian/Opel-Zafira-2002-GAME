import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
try:
    bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase')
    names=[]
    # no direct list vars? use dir
    for n in dir(u.BlueprintEditorLibrary):
        if 'variable' in n.lower(): names.append(n)
    out={'api':names}
    # try generated class cdo properties matching gear/transmission/auto
    cls=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira')
    cdo=u.get_default_object(cls)
    props=[]
    for p in dir(cdo):
        if any(s in p.lower() for s in ['gear','trans','throttle','brake','auto','speed']): props.append(p)
    out['cdo_dir_matches']=props[:200]
    for p in props:
        try: out[p]=str(cdo.get_editor_property(p))
        except Exception: pass
except Exception:
    out={'error':traceback.format_exc()}
(S/'zafira_variables_report.json').write_text(json.dumps(out,indent=2,default=str)); print(S/'zafira_variables_report.json')