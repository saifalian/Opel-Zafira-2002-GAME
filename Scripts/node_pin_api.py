import unreal as u, pathlib, json
bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase'); g=u.BlueprintGraphEditor.get_graph_editor_by_name(bp,'ZafiraTransmissionInput')
n=g.list_all_nodes()[0]
out=[x for x in dir(n) if 'pin' in x.lower() or 'default' in x.lower()]
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/node_pin_api.json'); path.write_text(json.dumps(out,indent=2)); print(path)
