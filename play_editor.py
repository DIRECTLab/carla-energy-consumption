# import unreal
# level_editor_subsystem.editor_request_begin_play()


# unreal.LevelEditorSubsystem().editor_play_simulate()


import pyautogui
import time
import subprocess

TIME_TO_WAIT = 100


subprocess.Popen(
    ["bash", "start_carla_server.sh"],
    stdout=subprocess.DEVNULL, 
    stderr=subprocess.DEVNULL
)

unreal_window_handle = None

while unreal_window_handle is None:
    try:
        unreal_window_handle_bytes = subprocess.check_output(
            ["xdotool", "search", "--name", "Unreal Editor"]
        ) 
        print(
            "TEST unreal_window_handle_bytes: ", 
            unreal_window_handle_bytes
        )
        unreal_window_handle = unreal_window_handle_bytes.split()[0]
        print("TEST unreal window handle: ", unreal_window_handle)
    except subprocess.CalledProcessError:
        print("Window not found yet")
        time.sleep(TIME_TO_WAIT)


subprocess.run(["xdotool", "windowactivate", unreal_window_handle])

time.sleep(1)
pyautogui.keyDown('alt')
pyautogui.press('p')
pyautogui.keyUp('alt')