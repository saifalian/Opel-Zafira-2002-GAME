import unreal as u, pathlib, json, traceback
ROOT=pathlib.Path('D:/unreal engine/project/ZafiraDrive')
SRC=ROOT/'SourceArt/TouchButtons'
DEST='/Game/VehicleTemplate/Input/TouchLabels'
report={'textures':[]}
try:
    tools=u.AssetToolsHelpers.get_asset_tools()
    tasks=[]
    for png in SRC.glob('*.png'):
        t=u.AssetImportTask(); t.filename=str(png); t.destination_path=DEST; t.destination_name='T_Button_'+png.stem; t.automated=True; t.save=True; t.replace_existing=True; tasks.append(t)
    tools.import_asset_tasks(tasks)
    for png in SRC.glob('*.png'):
        path=f'{DEST}/T_Button_{png.stem}'
        tex=u.EditorAssetLibrary.load_asset(path)
        if tex:
            try:
                tex.set_editor_property('compression_settings', u.TextureCompressionSettings.TC_EDITOR_ICON)
                tex.set_editor_property('srgb', True)
            except Exception: pass
            u.EditorAssetLibrary.save_asset(path)
        report['textures'].append(path)
    report['success']=True
except Exception:
    report['success']=False; report['error']=traceback.format_exc(); u.log_error(report['error'])
(ROOT/'Scripts/restyle_buttons_report.json').write_text(json.dumps(report,indent=2,default=str))
assert report.get('success'), report