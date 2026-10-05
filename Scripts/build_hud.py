import unreal as u,json,pathlib,shutil,traceback
R=pathlib.Path('D:/unreal engine/project/ZafiraDrive');S=R/'Scripts';r={};G=u.BlueprintGraphEditor;L=u.BlueprintEditorLibrary
src=R/'Content/VehicleTemplate/UI/UI_Vehicle.uasset';bk=S/'hud_backup';bk.mkdir(exist_ok=True)
if not (bk/src.name).exists():shutil.copy2(src,bk/src.name)
def link(a,b):
 assert a.is_valid() and b.is_valid(),'invalid pins'
 assert a.try_create_connection(b),'failed connection '+str(a.get_pin_name())+' '+str(b.get_pin_name())
def call(path,**vs):
 n=g.add_call_function_node(path if path.startswith('/') else '/Script/Engine.'+path);assert n,path
 for p,v in vs.items():n.find_input_pin(p).set_pin_value(str(v))
 return n
def out(n):return n.find_result_pin()
try:
 b=u.load_asset('/Game/VehicleTemplate/UI/UI_Vehicle');g=G.get_graph_editor_by_name(b,'EventGraph')
 pawn=call('GameplayStatics.GetPlayerPawn',PlayerIndex=0)
 comp=call('Actor.GetComponentByClass',ComponentClass='/Script/ChaosVehicles.ChaosWheeledVehicleMovementComponent');link(out(pawn),comp.find_self_pin())
 rpm=call('/Script/ChaosVehicles.ChaosWheeledVehicleMovementComponent.GetEngineRotationSpeed');link(out(comp),rpm.find_self_pin())
 auto=call('/Script/ChaosVehicles.ChaosVehicleMovementComponent.GetUseAutoGears');link(out(comp),auto.find_self_pin())
 rnd=call('KismetMathLibrary.Round');link(out(rpm),rnd.find_input_pin('A'))
 text=call('KismetStringLibrary.Conv_IntToString');link(out(rnd),text.find_input_pin('InInt'))
 cat=call('KismetStringLibrary.Concat_StrStr',A='km/h  |  RPM ');link(out(text),cat.find_input_pin('B'))
 mode=call('KismetMathLibrary.SelectString',A='  |  AUTO',B='  |  MANUAL');link(out(auto),mode.find_input_pin('bPickA'))
 cat2=call('KismetStringLibrary.Concat_StrStr');link(out(cat),cat2.find_input_pin('A'));link(out(mode),cat2.find_input_pin('B'))
 tx=call('KismetTextLibrary.Conv_StringToText');link(out(cat2),tx.find_input_pin('InString'))
 setter=call('/Script/UMG.TextBlock.SetText');link(out(tx),setter.find_input_pin('InText'));link(g.add_get_member_variable_node('UnitLabel').find_result_pin(),setter.find_self_pin())
 speed=next(n for n in g.list_all_nodes() if n.get_name()=='K2Node_CallFunction_2');link(speed.find_then_pin(),setter.find_execute_pin())
 unit=u.find_object(None,'/Game/VehicleTemplate/UI/UI_Vehicle.UI_Vehicle:WidgetTree.UnitLabel');unit.modify();f=unit.get_editor_property('font');f.set_editor_property('size',22);unit.set_editor_property('font',f)
 parent=unit.get_parent();r['parents']=[]
 while parent:
  slot=parent.get_editor_property('slot');r['parents'].append({'name':parent.get_name(),'class':parent.get_class().get_name(),'slot':str(slot)})
  if isinstance(slot,u.CanvasPanelSlot):
   slot.modify();slot.set_auto_size(True);slot.set_position(u.Vector2D(35,-150));slot.set_alignment(u.Vector2D(0,0));slot.set_anchors(u.Anchors(u.Vector2D(0,1),u.Vector2D(0,1)));break
  parent=parent.get_parent()
 L.compile_blueprint(b);errors=[n.get_node_title() for n in g.list_nodes_with_errors()];assert not errors,errors
 assert u.EditorAssetLibrary.save_loaded_asset(b,False);r.update(success=True,errors=errors)
except:r['error']=traceback.format_exc();u.log_error(r['error'])
(S/'hud_build_report.json').write_text(json.dumps(r,indent=2,default=str))
assert r.get('success'),r
