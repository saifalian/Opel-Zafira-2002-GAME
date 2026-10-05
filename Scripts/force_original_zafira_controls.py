import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
r={}
try:
    # Revert damage from previous experiments: use original vehicle pawn/controller and original working ZafiraTest map for control testing.
    zcls=E.load_blueprint_class('/Game/Zafira/BP_Zafira')
    pccls=E.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
    assert zcls and pccls, (zcls, pccls)
    for gm_path in ['/Game/Zafira/BP_ZafiraGameMode','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode']:
        bp=E.load_asset(gm_path); cls=E.load_blueprint_class(gm_path); cdo=u.get_default_object(cls); cdo.modify()
        cdo.set_editor_property('default_pawn_class', zcls)
        cdo.set_editor_property('player_controller_class', pccls)
        L.compile_blueprint(bp); E.save_loaded_asset(bp,False)
    # restore legacy and enhanced mappings to all likely input contexts using proper Key export names.
    def key(n):
        k=u.Key(); k.set_editor_property('key_name', u.Name(n)); return k
    def neg(outer): return u.new_object(u.InputModifierNegate, outer=outer)
    mapped={}
    for imc_path in ['/Game/VehicleTemplate/Input/IMC_Vehicle_Default','/Game/VehicleTemplate/Input/IMC_SteeringWheel','/Game/Input/IMC_Default']:
        imc=E.load_asset(imc_path)
        if not imc: continue
        imc.modify()
        try: imc.unmap_all()
        except Exception: pass
        entries=[]
        def add(action_path,key_name,negative=False):
            act=E.load_asset(action_path)
            if not act: return
            m=imc.map_key(act,key(key_name))
            if negative: m.set_editor_property('modifiers',[neg(imc)])
            entries.append((action_path,key_name,negative))
        add('/Game/VehicleTemplate/Input/Actions/IA_Throttle','W'); add('/Game/VehicleTemplate/Input/Actions/IA_Throttle','Up'); add('/Game/VehicleTemplate/Input/Actions/IA_Throttle','Gamepad_RightTriggerAxis')
        add('/Game/VehicleTemplate/Input/Actions/IA_Brake','S'); add('/Game/VehicleTemplate/Input/Actions/IA_Brake','Down'); add('/Game/VehicleTemplate/Input/Actions/IA_Brake','Gamepad_LeftTriggerAxis')
        add('/Game/VehicleTemplate/Input/Actions/IA_Steering','A',True); add('/Game/VehicleTemplate/Input/Actions/IA_Steering','Left',True)
        add('/Game/VehicleTemplate/Input/Actions/IA_Steering','D'); add('/Game/VehicleTemplate/Input/Actions/IA_Steering','Right'); add('/Game/VehicleTemplate/Input/Actions/IA_Steering','Gamepad_LeftX')
        add('/Game/VehicleTemplate/Input/Actions/IA_Handbrake','SpaceBar'); add('/Game/VehicleTemplate/Input/Actions/IA_Reset','R'); add('/Game/VehicleTemplate/Input/Actions/IA_ToggleCamera','C')
        E.save_loaded_asset(imc,False); mapped[imc_path]=len(entries)
    # Put ZafiraTest player start clear on flat ground; use it as known drivable base until movement confirmed.
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraTest')
    world=u.EditorLevelLibrary.get_editor_world(); ws=world.get_world_settings(); ws.modify(); ws.set_editor_property('default_game_mode', E.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode'))
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart':
            a.set_actor_location(u.Vector(0,0,420),False,False); a.set_actor_rotation(u.Rotator(0,0,0),False)
    ok=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraTest')
    r={'success':True,'mapped':mapped,'test_map_save':ok,'note':'Restored original real Zafira pawn/controller and input contexts; testing on original ZafiraTest flat map first.'}
except Exception:
    r={'success':False,'error':traceback.format_exc()}; u.log_error(r['error'])
(S/'force_original_zafira_controls_report.json').write_text(json.dumps(r,indent=2,default=str)); print(json.dumps(r,default=str))
assert r.get('success')