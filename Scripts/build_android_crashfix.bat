@echo off
cd /d "D:\unreal engine\UE_5.8\Engine\Build\BatchFiles"
call RunUAT.bat BuildCookRun -project="D:\unreal engine\project\ZafiraDrive\ZafiraDrive.uproject" -noP4 -platform=Android -clientconfig=Development -nocompileeditor -skipbuildeditor -cook -map=/Game/Zafira/Maps/ZafiraStraight5KM -build -stage -pak -archive -archivedirectory="D:\unreal engine\project\ZafiraDrive\BuildOutput\Android_Straight5KM_CrashFix" -package -prereqs -nodebuginfo
