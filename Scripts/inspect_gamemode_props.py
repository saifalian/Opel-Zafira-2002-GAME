import unreal as u, pathlib, json
E=u.EditorAssetLibrary
out={}
for path in ['/Game/Zafira/BP_ZafiraGameMode','/Game/VehicleTemplate/Blueprints/BP_VehicleAdvGameMode']:
    cls=E.load_blueprint_class(path); cdo=u.get_default_object(cls)
    out[path]={}
    for p in ['default_pawn_class','player_controller_class','hud_class','spectator_class']:
        try: out[path][p]=str(cdo.get_editor_property(p))
        except Exception as e: out[path][p]='ERR '+str(e)
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/gamemode_props.json'); path.write_text(json.dumps(out,indent=2)); print(path)
