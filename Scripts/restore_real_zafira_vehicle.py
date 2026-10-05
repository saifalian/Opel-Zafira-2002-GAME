import unreal as u, pathlib, json, traceback
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts'); E=u.EditorAssetLibrary; L=u.BlueprintEditorLibrary
report={}
try:
    zcls=E.load_blueprint_class('/Game/Zafira/BP_Zafira')
    pccls=E.load_blueprint_class('/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController')
    assert zcls, 'Missing /Game/Zafira/BP_Zafira class'
    # Restore real Zafira vehicle pawn and original vehicle controller so diesel/audio/control blueprint path is used.
    for gm_path in ['/Game/Zafira/BP_ZafiraGameMode','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode']:
        gm=E.load_asset(gm_path); gmcls=E.load_blueprint_class(gm_path); cdo=u.get_default_object(gmcls); cdo.modify()
        cdo.set_editor_property('default_pawn_class', zcls)
        if pccls: cdo.set_editor_property('player_controller_class', pccls)
        L.compile_blueprint(gm); E.save_loaded_asset(gm,False)
    # Ensure vehicle enhanced input mappings are not empty.
    def key(name):
        k=u.Key(); k.set_editor_property('key_name', name); return k
    def neg(outer): return u.new_object(u.InputModifierNegate, outer=outer)
    imc=E.load_asset('/Game/VehicleTemplate/Input/IMC_Vehicle_Default')
    mapped=[]
    if imc:
        imc.modify(); imc.unmap_all()
        acts={n:E.load_asset('/Game/VehicleTemplate/Input/Actions/IA_'+n) for n in ['Throttle','Brake','Steering','Handbrake','Reset','ToggleCamera','LookAround']}
        def add(a,k,negative=False):
            act=acts.get(a)
            if not act: return
            m=imc.map_key(act,key(k))
            if negative: m.set_editor_property('modifiers',[neg(imc)])
            mapped.append((a,k,negative))
        for k in ['W','Up','Gamepad_RightTriggerAxis']: add('Throttle',k)
        for k in ['S','Down','Gamepad_LeftTriggerAxis']: add('Brake',k)
        for k in ['A','Left']: add('Steering',k,True)
        for k in ['D','Right','Gamepad_LeftX']: add('Steering',k)
        add('Handbrake','SpaceBar'); add('Handbrake','Gamepad_FaceButton_Bottom')
        add('Reset','R'); add('ToggleCamera','C'); add('ToggleCamera','Gamepad_Special_Left')
        E.save_loaded_asset(imc,False)
    # Put PlayerStart on a clear part of the visible road and higher enough for the real vehicle spawn collision.
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraPlayableTrack')
    world=u.EditorLevelLibrary.get_editor_world(); ws=world.get_world_settings(); ws.modify()
    gmcls=E.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode')
    if gmcls: ws.set_editor_property('default_game_mode', gmcls)
    changed=[]
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if a.get_class().get_name()=='PlayerStart':
            a.modify(); a.set_actor_location(u.Vector(1800,0,820),False,False); a.set_actor_rotation(u.Rotator(0,0,0),False); changed.append(a.get_name())
    ok=u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Zafira/Maps/ZafiraPlayableTrack')
    report={'success':True,'restored_real_vehicle':'/Game/Zafira/BP_Zafira','controller':'/Game/VehicleTemplate/Blueprints/BP_VehicleAdvPlayerController' if pccls else 'default/missing','mapped_count':len(mapped),'playerstart':[1800,0,820],'save_map':ok}
except Exception:
    report={'success':False,'error':traceback.format_exc()}; u.log_error(report['error'])
(S/'restore_real_zafira_vehicle_report.json').write_text(json.dumps(report,indent=2,default=str)); print(json.dumps(report,default=str))
assert report.get('success')