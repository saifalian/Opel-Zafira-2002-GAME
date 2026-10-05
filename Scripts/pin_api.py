import unreal as u, pathlib, json
bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase'); g=u.BlueprintGraphEditor.get_graph_editor_by_name(bp,'ZafiraTransmissionInput')
for n in g.list_all_nodes():
    if 'WasInput' in str(n.get_node_title()):
        p=n.list_all_pins()[0]; break
out=[x for x in dir(p) if not x.startswith('_')]
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/pin_api.json'); path.write_text(json.dumps(out,indent=2)); print(path)
