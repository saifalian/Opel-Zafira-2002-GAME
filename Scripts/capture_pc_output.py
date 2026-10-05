import unreal as u, pathlib, json, time, traceback
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
OUT=ROOT/'Scripts/pc_output_capture.json'
SHOT='D:/unreal engine/project/ZafiraDrive/Saved/Screenshots/WindowsEditor/Zafira_PC_Output.png'
state={'started':False,'t':0,'busy':False,'shot':False}
report={}
sub=u.get_editor_subsystem(u.LevelEditorSubsystem)
try:
    u.EditorLevelLibrary.load_level('/Game/Zafira/Maps/ZafiraLongTrack')
except Exception as e:
    report['load_error']=traceback.format_exc()

def finish(err=None):
    report['success']=err is None
    if err: report['error']=err
    report['screenshot']=SHOT
    OUT.write_text(json.dumps(report,indent=2,default=str))
    try: sub.editor_request_end_play()
    except Exception: pass
    try: u.unregister_slate_post_tick_callback(handle)
    except Exception: pass
    u.SystemLibrary.quit_editor()

def tick(dt):
    if state['busy']: return
    state['busy']=True
    try:
        state['t']+=dt
        if state['t']>30: finish('timeout'); return
        if not state['started']:
            state['started']=True
            sub.editor_request_begin_play()
            return
        w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
        if not w: return
        pc=u.GameplayStatics.get_player_controller(w,0)
        if not pc: return
        pawn=pc.get_controlled_pawn()
        if pawn:
            report['pawn']=pawn.get_name()
            report['pawn_loc']=str(pawn.get_actor_location())
            m=pawn.get_component_by_class(u.ChaosWheeledVehicleMovementComponent)
            if m:
                m.set_throttle_input(0.25 if state['t']<5 else 0)
                report['speed_kmh']=abs(m.get_forward_speed())*.036
        if state['t']>5 and not state['shot']:
            state['shot']=True
            u.SystemLibrary.execute_console_command(w,'DisableAllScreenMessages',pc)
            u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename=D:/unreal engine/project/ZafiraDrive/Saved/Screenshots/WindowsEditor/Zafira_PC_Output.png',pc)
        if state['t']>8: finish()
    except Exception:
        finish(traceback.format_exc())
    finally:
        state['busy']=False
handle=u.register_slate_post_tick_callback(tick)
