import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
r=[]
try:
    bp=u.load_asset('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPawnBase')
    g=u.BlueprintGraphEditor.get_graph_editor_by_name(bp,'ZafiraTransmissionInput')
    for n in g.list_all_nodes():
        title=str(n.get_node_title())
        if 'WasInput' in title or 'Key' in title or 'Input' in title:
            item={'node':n.get_name(),'title':title,'class':n.get_class().get_name(),'pins':[]}
            for p in n.list_all_pins():
                item['pins'].append({'name':str(p.get_pin_name()),'direction':str(p.get_pin_direction()),'value':str(p.get_pin_value()),'type':str(p.get_pin_type_display_string())})
            r.append(item)
except Exception:
    r={'error':traceback.format_exc()}
(S/'transmission_nodes_pins.json').write_text(json.dumps(r,indent=2,default=str)); print(S/'transmission_nodes_pins.json')