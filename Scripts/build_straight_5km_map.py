import unreal as u, pathlib, json, traceback, math
S=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts')
OUT='/Game/Zafira/Maps/ZafiraStraight5KM'
report={}
try:
    # Start from the known visible/original real-Zafira map so vehicle/controller/HUD stay intact.
    world=u.EditorLoadingAndSavingUtils.load_map('/Game/Zafira/Maps/ZafiraTest')
    u.EditorLevelLibrary.save_current_level()
    # Duplicate by saving current loaded map to new package.
    world=u.EditorLevelLibrary.get_editor_world()

    def mat(name, color, rough=0.75):
        path='/Game/Zafira/Straight5KM/'+name
        m=u.load_asset(path)
        if not m:
            asset_tools=u.AssetToolsHelpers.get_asset_tools()
            m=asset_tools.create_asset(name, '/Game/Zafira/Straight5KM', u.Material, None)
        try:
            m.set_editor_property('blend_mode', u.BlendMode.BLEND_OPAQUE)
            m.set_editor_property('shading_model', u.MaterialShadingModel.MSM_DEFAULT_LIT)
            u.MaterialEditingLibrary.set_material_usage(m, u.MaterialUsage.MATUSAGE_STATIC_LIGHTING)
            u.MaterialEditingLibrary.set_material_usage(m, u.MaterialUsage.MATUSAGE_INSTANCED_STATIC_MESHES)
            base=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant3Vector,-400,0)
            base.constant=color
            u.MaterialEditingLibrary.connect_material_property(base,'',u.MaterialProperty.MP_BASE_COLOR)
            r=u.MaterialEditingLibrary.create_material_expression(m,u.MaterialExpressionConstant,-400,120)
            r.r=rough
            u.MaterialEditingLibrary.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
            u.MaterialEditingLibrary.recompile_material(m)
            u.EditorAssetLibrary.save_loaded_asset(m,False)
        except Exception:
            pass
        return m

    road_m=mat('M_S5_Road',u.LinearColor(0.10,0.105,0.11,1))
    grass_m=mat('M_S5_Floor',u.LinearColor(0.18,0.25,0.16,1))
    line_m=mat('M_S5_WhiteLines',u.LinearColor(0.95,0.95,0.90,1))
    barrier_m=mat('M_S5_BarrierYellow',u.LinearColor(0.95,0.65,0.05,1))
    wall_m=mat('M_S5_Wall',u.LinearColor(0.48,0.48,0.50,1))
    mark_m=mat('M_S5_KMMarkers',u.LinearColor(0.02,0.02,0.02,1))

    cube=u.load_asset('/Engine/BasicShapes/Cube.Cube')
    # Clear previous straight-map actors if re-running.
    for a in list(u.EditorLevelLibrary.get_all_level_actors()):
        if a.get_actor_label().startswith('S5_'):
            u.EditorLevelLibrary.destroy_actor(a)

    def cube_actor(label, loc, scale, material):
        a=u.EditorLevelLibrary.spawn_actor_from_object(cube, u.Vector(*loc), u.Rotator(0,0,0))
        a.set_actor_label(label)
        a.set_actor_scale3d(u.Vector(*scale))
        comp=a.get_component_by_class(u.StaticMeshComponent)
        if comp:
            comp.set_static_mesh(cube)
            comp.set_material(0, material)
            comp.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS)
            comp.set_collision_profile_name('BlockAll')
        return a

    # Coordinate system: 5km along +X. Unreal cm units => 500000 cm.
    length=500000.0
    seg_len=25000.0  # 250m chunks
    road_w=1800.0
    floor_w=7000.0
    z=0.0
    start_x=0.0
    # Long floor exactly like a flat/simple plane, but much longer.
    for i in range(int(length/seg_len)):
        x=start_x+i*seg_len+seg_len/2
        cube_actor(f'S5_Floor_{i:02d}', (x,0,-25), (seg_len/100.0, floor_w/100.0, 0.08), grass_m)
        cube_actor(f'S5_Road_{i:02d}', (x,0,4), (seg_len/100.0, road_w/100.0, 0.08), road_m)
        # side road shoulder/curbs
        cube_actor(f'S5_Left_Curb_{i:02d}', (x,-road_w/2-40,25), (seg_len/100.0,0.28,0.18), barrier_m)
        cube_actor(f'S5_Right_Curb_{i:02d}', (x,road_w/2+40,25), (seg_len/100.0,0.28,0.18), barrier_m)
        # tall walls/boundary; physically block car from leaving map/road area
        cube_actor(f'S5_Left_Wall_{i:02d}', (x,-floor_w/2,160), (seg_len/100.0,0.55,3.2), wall_m)
        cube_actor(f'S5_Right_Wall_{i:02d}', (x,floor_w/2,160), (seg_len/100.0,0.55,3.2), wall_m)
        # Road barriers closer to road edges
        cube_actor(f'S5_Left_Barrier_{i:02d}', (x,-road_w/2-180,80), (seg_len/100.0,0.35,1.0), barrier_m)
        cube_actor(f'S5_Right_Barrier_{i:02d}', (x,road_w/2+180,80), (seg_len/100.0,0.35,1.0), barrier_m)
        # dashed center lines every 250m segment
        for j in range(5):
            lx=x-seg_len/2+j*5000+1500
            cube_actor(f'S5_CenterLine_{i:02d}_{j}', (lx,0,16), (18,0.10,0.025), line_m)

    # Start/finish wall behind start and end boundary so car cannot escape ends.
    cube_actor('S5_Start_Back_Wall', (-900,-0,180), (0.6,floor_w/100.0,3.6), wall_m)
    cube_actor('S5_End_Wall', (length+800,0,180), (0.6,floor_w/100.0,3.6), wall_m)

    # Kilometer text signs on both sides: 1KM PASS ... 5KM PASS
    font=None
    try: font=u.load_asset('/Engine/EngineFonts/Roboto.Roboto')
    except Exception: pass
    text_rows=[]
    for km in range(1,6):
        x=km*100000.0
        for side,yaw,y in [('L',90,-road_w/2-650),('R',-90,road_w/2+650)]:
            t=u.EditorLevelLibrary.spawn_actor_from_class(u.TextRenderActor, u.Vector(x,y,230), u.Rotator(0,yaw,0))
            t.set_actor_label(f'S5_{km}KM_PASS_{side}')
            comp=t.get_component_by_class(u.TextRenderComponent)
            if comp:
                comp.set_text(f'{km} KM PASS')
                comp.set_world_size(420)
                try: comp.set_horizontal_alignment(u.HorizTextAligment.EHTA_CENTER)
                except Exception: pass
                try: comp.set_vertical_alignment(u.VerticalTextAligment.EVRTA_TEXT_CENTER)
                except Exception: pass
                comp.set_text_render_color(u.Color(255,245,30,255))
                if font: comp.set_font(font)
            text_rows.append(t.get_actor_label())
        # Big overhead gate marker, also blocks/scenery but leaves road opening
        cube_actor(f'S5_{km}KM_Gantry_LeftPost', (x,-road_w/2-350,350), (0.55,0.55,6.5), barrier_m)
        cube_actor(f'S5_{km}KM_Gantry_RightPost', (x,road_w/2+350,350), (0.55,0.55,6.5), barrier_m)
        cube_actor(f'S5_{km}KM_Gantry_Top', (x,0,680), (0.6,(road_w+900)/100.0,0.45), barrier_m)

    # Place real player start on center of straight road, facing +X.
    for a in u.EditorLevelLibrary.get_all_level_actors():
        if isinstance(a,u.PlayerStart):
            a.set_actor_label('S5_PlayerStart')
            a.set_actor_location(u.Vector(700,0,130), False, False)
            a.set_actor_rotation(u.Rotator(0,0,0), False)
            break
    else:
        ps=u.EditorLevelLibrary.spawn_actor_from_class(u.PlayerStart,u.Vector(700,0,130),u.Rotator(0,0,0))
        ps.set_actor_label('S5_PlayerStart')

    # Ensure this map still uses the real Zafira game mode if world settings supports it.
    gm=u.EditorAssetLibrary.load_blueprint_class('/Game/Zafira/BP_ZafiraGameMode')
    try:
        u.EditorLevelLibrary.get_editor_world().get_world_settings().set_editor_property('default_game_mode', gm)
    except Exception as e:
        report['gamemode_warning']=str(e)

    ok=u.EditorLoadingAndSavingUtils.save_map(u.EditorLevelLibrary.get_editor_world(), OUT)
    report.update({'success':bool(ok),'map':OUT,'length_cm':length,'length_km':5.0,'road_width_cm':road_w,'floor_width_cm':floor_w,'km_markers':text_rows})
except Exception:
    report={'success':False,'error':traceback.format_exc()}
    u.log_error(report['error'])
(S/'straight_5km_report.json').write_text(json.dumps(report,indent=2,default=str))
print(json.dumps(report,default=str))
