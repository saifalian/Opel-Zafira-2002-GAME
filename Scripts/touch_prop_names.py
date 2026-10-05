import unreal as u,json,pathlib
c=u.TouchInputControl(); r={}
for p in ['bTreatAsButton','treat_as_button','b_treat_as_button','image1','Image1','center','Center','visual_size','VisualSize','main_input_key','MainInputKey']:
    try:
        c.get_editor_property(p); r[p]='ok'
    except Exception as e: r[p]=str(e).split('\n')[0]
pathlib.Path('D:/unreal engine/project/ZafiraDrive/Scripts/touch_prop_names.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))