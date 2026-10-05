Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdcBlt, uint nFlags);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
 [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
"@
Add-Type -AssemblyName System.Drawing
$p = Get-Process UnrealEditor -ErrorAction SilentlyContinue | Where-Object {$_.MainWindowTitle -like "ZafiraDrive*"} | Select-Object -First 1
if (-not $p) { throw "No UnrealEditor ZafiraDrive window found" }
[Win32]::ShowWindow($p.MainWindowHandle,9) | Out-Null
$r = New-Object Win32+RECT
[Win32]::GetWindowRect($p.MainWindowHandle, [ref]$r) | Out-Null
$w = [Math]::Max(1, $r.Right - $r.Left)
$h = [Math]::Max(1, $r.Bottom - $r.Top)
$bmp = New-Object System.Drawing.Bitmap $w,$h
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
[Win32]::PrintWindow($p.MainWindowHandle, $hdc, 2) | Out-Null
$g.ReleaseHdc($hdc)
$g.Dispose()
$path = "D:/unreal engine/project/ZafiraDrive/Scripts/unreal_window_capture.png"
$bmp.Save($path,[System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
Write-Output $path
Write-Output "title=$($p.MainWindowTitle) hwnd=$($p.MainWindowHandle) size=${w}x${h} rect=$($r.Left),$($r.Top),$($r.Right),$($r.Bottom)"
