# AI Coding Instructions

## Python Environment
When running Python commands in this repository, prefer the repository virtual environment if it exists.
On Windows PowerShell, use:
```powershell
$py = if (Test-Path .\.venv\Scripts\python.exe) { ".\.venv\Scripts\python.exe" } else { "python" }
& $py -m pytest
```

## Project Structure
- `src/config.py` - Main configuration (window settings, OCR, template matching, task registration)
- `src/task/DailyTask.py` - One-click daily routine task
- `src/task/SkipDialogTask.py` - Auto-skip dialog trigger task
- `src/task/AutoLoginTask.py` - Auto-login trigger task
- `src/scene/INScene.py` - Scene detection for Infinity Nikki
- `assets/` - Template matching images (coco_annotations.json)
- `i18n/` - Internationalization files

## Key References
- ok-script API: https://github.com/ok-oldking/ok-script/blob/master/docs/api_doc/README.md
- ok-script Quick Start: https://github.com/ok-oldking/ok-script/blob/master/docs/quick_start/README.md
- Reference project (Wuthering Waves): https://github.com/ok-oldking/ok-wuthering-waves
- Reference project (NTE): https://github.com/BnanZ0/ok-nte

## Game Technical Details
- Game executable: X6Game-Win64-Shipping.exe
- Window class: UnrealWindow (Unreal Engine game)
- Launcher: InfinityNikki Launcher.exe
- Anti-cheat: Anti-Cheat Expert (ACE) - ok-script uses PostMessage for input simulation
- Background support: Yes (PostMessage interaction mode)

## Development Notes
- Use `find_feature` / `wait_feature` / `wait_click_feature` for image-based interactions
- Use `ocr` / `wait_ocr` / `wait_click_ocr` for text-based interactions
- Prefer `wait_*` methods over manual `sleep` + check patterns
- All feature names must have corresponding entries in `assets/coco_annotations.json`
- The game uses 16:9 aspect ratio; ensure template images are captured at 1920x1080
