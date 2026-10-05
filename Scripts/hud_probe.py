import unreal as u,json,pathlib,traceback
r={}
try:
 b=u.load_asset('/Game/VehicleTemplate/UI/UI_Vehicle');r['vars']=list(u.BlueprintEditorLibrary.list_member_variable_names(b));r['graphs']={}
 for name in u.BlueprintEditorLibrary.list_graph_names(b):
  g=u.BlueprintGraphEditor.get_graph_editor_by_name(b,name);r['graphs'][str(name)]=[{'title':n.get_node_title(),'name':n.get_name(),'pins':[{'name':str(p.get_pin_name()),'value':p.get_pin_value(),'links':[q.get_owning_node().get_name()+':'+str(q.get_pin_name()) for q in p.list_connected_pins()]} for p in n.list_all_pins()]} for n in g.list_all_nodes()]
 r['api']=[s for s in dir(u.BlueprintGraphEditor) if not s.startswith('_')]
 r['widget_api']=[s for s in dir(u) if 'Widget' in s and ('Editor' in s or 'Blueprint' in s)]
except:r['error']=traceback.format_exc()
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/hud_probe.json').write_text(json.dumps(r,indent=2,default=str))
