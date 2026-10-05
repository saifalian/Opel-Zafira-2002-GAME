import unreal as u,json,pathlib
r={}
for c in [u.BlueprintEditorLibrary,u.BlueprintGraphEditor,u.SubobjectDataSubsystem]:
 r[c.__name__]={n:getattr(c,n).__doc__ for n in dir(c) if any(s in n.lower() for s in ['type','subobject','component'])}
b=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase');g=u.BlueprintGraphEditor.get_graph_editor_by_name(b,'EventGraph');r['nodes']=[(n.get_name(),n.get_node_title()) for n in g.list_all_nodes()]
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/audio_probe.json').write_text(json.dumps(r,indent=2))
