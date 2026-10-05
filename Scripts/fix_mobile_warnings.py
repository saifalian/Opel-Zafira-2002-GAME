import unreal as u, pathlib, json, traceback
P=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
report={'removed':[],'changed':[]}
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraStraight5KM')
    world=u.EditorLevelLibrary.get_editor_world()
    # Remove mobile-problem SkyAtmosphere actors causing the red IsSky mesh warning.
    for actor in list(u.EditorLevelLibrary.get_all_level_actors()):
        cls=actor.get_class().get_name()
        name=actor.get_name()
        if 'SkyAtmosphere' in cls or 'SkyAtmosphere' in name:
            u.EditorLevelLibrary.destroy_actor(actor)
            report['removed'].append([name,cls])
            continue
        # Make lighting dynamic/mobile-safe so stale baked lighting warnings are not produced.
        if any(x in cls for x in ['DirectionalLight','SkyLight','PointLight','SpotLight','RectLight']):
            try:
                comp=actor.get_component_by_class(u.LightComponent)
                if comp:
                    comp.set_editor_property('mobility', u.ComponentMobility.MOVABLE)
                    report['changed'].append([name,cls,'light_movable'])
            except Exception as e:
                report['changed'].append([name,cls,'light_movable_error',str(e)])
    ws=world.get_world_settings()
    for prop,val in [('force_no_precomputed_lighting',True),('precompute_visibility',False)]:
        try:
            ws.set_editor_property(prop,val)
            report['changed'].append(['WorldSettings',prop,val])
        except Exception as e:
            report['changed'].append(['WorldSettings',prop,'error',str(e)])
    # Add a simple mobile-safe sky color/backdrop via exponential height fog if possible.
    try:
        fog=u.EditorLevelLibrary.spawn_actor_from_class(u.ExponentialHeightFog, u.Vector(0,0,0), u.Rotator(0,0,0))
        fog.set_actor_label('MobileSafe_BlueSky_Fog')
        comp=fog.get_component_by_class(u.ExponentialHeightFogComponent)
        if comp:
            comp.set_editor_property('fog_density',0.0004)
            comp.set_editor_property('fog_height_falloff',0.05)
            comp.set_editor_property('fog_inscattering_color',u.LinearColor(0.45,0.62,0.95,1))
        report['changed'].append(['spawned','MobileSafe_BlueSky_Fog'])
    except Exception as e:
        report['changed'].append(['fog_error',str(e)])
    u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    u.EditorLevelLibrary.save_current_level()
    report['success']=True
except Exception:
    report={'success':False,'error':traceback.format_exc()}
    u.log_error(report['error'])
(P/'Scripts/fix_mobile_warnings_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))