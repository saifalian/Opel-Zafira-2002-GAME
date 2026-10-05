import pathlib, re
p=pathlib.Path('D:/unreal engine/project/ZafiraDrive/Config/DefaultEngine.ini')
s=p.read_text()
# Add/replace mobile-safe renderer CVars for Android crash: Null UAV on FMobileBasePassUniformParameters.
renderer='[/Script/Engine.RendererSettings]'
mobile_lines={
 'r.MobileHDR':'False',
 'r.Mobile.ShadingPath':'0',
 'r.Mobile.Forward.EnableLocalLights':'0',
 'r.Mobile.AllowDeferredShadingOpenGL':'0',
 'r.Mobile.VirtualTextures':'0',
 'r.VirtualTextures':'False',
 'r.ReflectionMethod':'0',
 'r.DynamicGlobalIlluminationMethod':'0',
 'r.GenerateMeshDistanceFields':'False',
 'r.RayTracing':'False',
 'r.SkinCache.CompileShaders':'False',
 'r.Shadow.Virtual.Enable':'0',
 'r.DefaultFeature.AutoExposure':'False',
 'r.DefaultFeature.MotionBlur':'False',
 'r.AllowStaticLighting':'True'
}
for k,v in mobile_lines.items():
    if re.search(rf'(?m)^{re.escape(k)}=', s):
        s=re.sub(rf'(?m)^{re.escape(k)}=.*$', f'{k}={v}', s)
    else:
        s=s.replace(renderer, renderer+'\n'+f'{k}={v}',1)
android='[/Script/AndroidRuntimeSettings.AndroidRuntimeSettings]'
android_lines={
 'bBuildForES31':'true',
 'bSupportsVulkan':'false',
 'bSupportsVulkanSM5':'false',
 'bDetectVulkanByDefault':'false',
 'bEnableRayTracing':'false',
 'bPackageDataInsideApk':'false',
 'Orientation':'SensorLandscape',
 'bBuildForArm64':'true'
}
if android not in s:
    s+='\n\n'+android+'\n'
for k,v in android_lines.items():
    if re.search(rf'(?m)^{re.escape(k)}=', s):
        s=re.sub(rf'(?m)^{re.escape(k)}=.*$', f'{k}={v}', s)
    else:
        idx=s.find(android)+len(android)
        s=s[:idx]+'\n'+f'{k}={v}'+s[idx:]
p.write_text(s)
print('patched mobile-safe Android renderer settings')