import unreal as u,json,pathlib,traceback
r=[]
try:
 cls=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_Zafira')
 cdo=u.get_default_object(cls)
 for comp in cdo.get_components_by_class(u.ActorComponent):
  d={'name':comp.get_name(),'class':comp.get_class().get_name()}
  for prop in ['relative_location','relative_rotation','target_arm_length','socket_offset','field_of_view','auto_activate']:
   try: d[prop]=str(comp.get_editor_property(prop))
   except Exception: pass
  r.append(d)
except Exception: r=[{'error':traceback.format_exc()}]
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/zafira_components.json').write_text(json.dumps(r,indent=2,default=str))
print(json.dumps(r,indent=2,default=str))