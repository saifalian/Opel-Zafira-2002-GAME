import unreal as u, pathlib, json, traceback
assets=['/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController','/Game/Zafira/BP_Zafira','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase']
r={}
for asset in assets:
    try:
        bp=u.load_asset(asset); graphs=u.BlueprintEditorLibrary.list_graph_names(bp); arr=[]
        for gn in graphs:
            try:
                g=u.BlueprintGraphEditor.get_graph_editor_by_name(bp,str(gn))
                for n in g.list_all_nodes():
                    title=str(n.get_node_title())
                    if any(s in title.lower() for s in ['mapping','input','throttle','brake','steering','beginplay','possess','context']):
                        arr.append({'graph':str(gn),'name':n.get_name(),'title':title,'class':n.get_class().get_name()})
            except Exception: pass
        r[asset]=arr
    except Exception as e: r[asset]=str(e)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/control_nodes_report.json'); path.write_text(json.dumps(r,indent=2)); print(path)
