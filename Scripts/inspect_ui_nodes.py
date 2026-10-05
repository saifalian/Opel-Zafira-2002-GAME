import unreal as u,json,pathlib,traceback
assets=['/Game/VehicleTemplate/Input/UI_Touch_Vehicle','/Game/VehicleTemplate/UI/UI_Vehicle','/Game/Zafira/BP_ZafiraGameMode','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController']
r={}
for a in assets:
 try:
  b=u.load_asset(a); g=u.BlueprintGraphEditor.get_graph_editor_by_name(b,'EventGraph'); arr=[]
  for n in g.list_all_nodes():
   title=str(n.get_node_title())
   if any(s in title.lower() for s in ['touch','hud','widget','viewport','interface','joystick','button']): arr.append({'name':n.get_name(),'title':title,'class':n.get_class().get_name()})
  r[a]=arr
 except Exception as e: r[a]=str(e)
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/ui_nodes.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))