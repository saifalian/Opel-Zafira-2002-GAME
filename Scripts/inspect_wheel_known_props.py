import unreal as u, pathlib, json
out={}
for p in ['/Game/Zafira/BP_WheelsFront','/Game/Zafira/BP_WheelsRear']:
    cls=u.EditorAssetLibrary.load_blueprint_class(p); cdo=u.get_default_object(cls)
    data={'class':cdo.get_class().get_name()}
    for prop in ['wheel_radius','wheel_width','cornering_stiffness','friction_force_multiplier','side_slip_modifier','slip_threshold','skid_threshold','max_steer_angle','affected_by_engine','affected_by_brake','affected_by_handbrake','axle_type','spring_rate','spring_preload','suspension_max_raise','suspension_max_drop','wheel_load_ratio']:
        try: data[prop]=str(cdo.get_editor_property(prop))
        except Exception as e: data[prop]='ERR '+str(e)
    out[p]=data
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/wheel_known_props.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
