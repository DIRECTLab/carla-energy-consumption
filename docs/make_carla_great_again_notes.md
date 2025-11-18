# Notes on Carla Work

This was the output after I put in a startup script into the Unreal editor, so that does work! I just need to get it to import properly

```bash
[2025.11.18-18.56.28:995][  1]LogPython: Error: Traceback (most recent call last):
[2025.11.18-18.56.28:995][  1]LogPython: Error:   File "/home/carla/carla-energy-consumption/play_editor.py", line 1, in <module>
[2025.11.18-18.56.28:995][  1]LogPython: Error:     from unreal import level_editor_subsystem
[2025.11.18-18.56.28:995][  1]LogPython: Error: ImportError: cannot import name 'level_editor_subsystem' from 'unreal' (unknown location)
```

## Got this bad boy working nicely for the one command run wonder

### Needed to install on system

install xdootool
install scrot

### Needed to install into conda env for client

* `opencv`
* `pyautogui`
