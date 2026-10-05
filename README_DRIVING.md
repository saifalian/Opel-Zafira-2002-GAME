# Zafira driving prototype

Launch: Drive_Zafira.cmd (uses the installed Unreal editor in game mode; not a packaged standalone executable).
Click inside the game window to capture input.
W / Up: throttle. S / Down: brake, then automatic reverse when held after stopping.
A/D: steer. Space: handbrake. Tab: camera. Backspace: reset. Alt+F4: close game.

Source appearance model remains D:/blender/project/zafira/downloaded/zafira_downloaded.blend, unchanged.
Model credit: 2002 Opel Zafira by tonielpro520, advertised CC BY 4.0; original attribution in D:/blender/project/zafira/driving/assets/ATTRIBUTION.txt.

VERIFIED: real PIE Chaos physics using direct movement inputs, 608 telemetry samples over 91.97 simulation seconds. 0-100 km/h 11.48 s; max observed 178.14 km/h; five forward gears, braking through near-zero speed into reverse, and steering response. Four wheel contacts and suspension forces recorded. Automated input test disables the controller requirement only in the test instance. Keyboard mappings read from UE5.8 DefaultKeyMappings; standalone game launched. Manual keyboard driving was attempted but not conclusively verified because foreground focus could not be held reliably. Desktop game appearance was inspected; clean saved engine screenshot capture did not succeed.

NOT COMPLETE factory simulation: published top speed 187 km/h not reached in tested run; suspension spring/damper rates estimated (front 300 and rear 260 N/cm, damping ratio .65), collision/animation retains Epic vehicle template chassis. Rear torsion-beam coupling is not specifically modelled. Gear ratios reflect five-speed manual but shifting and reverse are assisted/automatic. Curb mass 1485 kg provisional because published values conflict. Effective game drag .23 is a calibration value, not asserted factory Cd. No calibrated diesel audio, clutch simulation, damage system, working gauges, or bump-course validation claimed. Source visual lamp materials simplified for UE. Moving wheel visual alignment still needs dynamic review.

Research, scripts and test outputs: D:/blender/project/zafira/driving/
Authoritative most recent measured report: driving_results.json; samples: driving_telemetry.json.
