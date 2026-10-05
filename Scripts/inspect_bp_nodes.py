import unreal as u,json,pathlib,traceback
b=u.load_asset('/Game/Zafira/BP_Zafira')
r={}
try:
 g=u.BlueprintGraphEditor.get_graph_editor_by_name(b,'EventGraph')
 r['nodes']=[]
 for n in g.list_all_nodes():
  title=str(n.get_node_title())
  if any(s in title.lower() for s in ['touch','hud','widget','virtual','interface','create widget','add to viewport']):
   r['nodes'].append({'name':n.get_name(),'title':title,'class':n.get_class().get_name()})
except Exception: r['err']=traceback.format_exc()
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/bp_nodes.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))