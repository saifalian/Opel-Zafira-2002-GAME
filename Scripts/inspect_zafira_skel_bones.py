import unreal as u, pathlib, json, traceback
out={}
try:
    bp=u.load_asset('/Game/Zafira/BP_Zafira')
    ss=u.get_engine_subsystem(u.SubobjectDataSubsystem); lib=u.SubobjectDataBlueprintFunctionLibrary
    for h in ss.k2_gather_subobject_data_for_blueprint(bp):
        o=lib.get_object(lib.get_data(h))
        if isinstance(o,u.SkeletalMeshComponent):
            sm=o.get_editor_property('skeletal_mesh')
            rows={'component':o.get_name(),'mesh':str(sm)}
            try: rows['bones']=[str(x) for x in sm.get_editor_property('skeleton').get_reference_pose().get_bone_names()]
            except Exception as e: rows['bones_err']=str(e)
            try: rows['sockets']=[s.get_name() for s in sm.get_sockets()]
            except Exception as e: rows['sockets_err']=str(e)
            out[o.get_name()]=rows
except Exception: out={'error':traceback.format_exc()}
path=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/zafira_skel_bones.json'); path.write_text(json.dumps(out,indent=2,default=str)); print(path)
