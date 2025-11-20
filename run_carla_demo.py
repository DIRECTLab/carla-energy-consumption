from time import sleep
from pyautogui import (
    keyDown, 
    press, 
    keyUp, 
    locateOnScreen, 
    ImageNotFoundException
)
from subprocess import (
    DEVNULL,
    check_output, 
    CalledProcessError, 
    run as run_sub_process, 
    Popen
)

PATH_TO_HELPER_SCRIPTS = "./demo_helper_scripts"
PATH_TO_UI_IMAGE = "./docs/figures/carlaUE4-play-btn.png"
WINDOW_NAME = "CarlaUE4 - Unreal Editor"

IMAGE_CONFIDENCE = 0.8

EXPECTED_TIME_UNTIL_WINDOW_APPEARANCE = 70
RETRY_WINDOW = 5
WAIT_BEFORE_CLIENT_START = 30



Popen(
    ["bash", "run_server.sh"],
    cwd=PATH_TO_HELPER_SCRIPTS,
    stdout=DEVNULL, 
    stderr=DEVNULL
)

print("Waiting for window to appear")
sleep(EXPECTED_TIME_UNTIL_WINDOW_APPEARANCE)

print("Checking for window")
unreal_window_handle = None
while unreal_window_handle is None:
    try:
        unreal_window_handle_bytes = check_output(
            ["xdotool", "search", "--onlyvisible", "--name", WINDOW_NAME]
        ) 
        unreal_window_handle = unreal_window_handle_bytes.split()[0]
    except CalledProcessError:
        sleep(RETRY_WINDOW)


print("Searching for image...")
image_found = False
while not image_found:
    try: 
        image_found = locateOnScreen(image=PATH_TO_UI_IMAGE, confidence=IMAGE_CONFIDENCE)
        print("image_found output: ", image_found)
    except ImageNotFoundException:
        print("Waiting to load...")
        sleep(RETRY_WINDOW)

print("FOCUS")
run_sub_process(["xdotool", "windowfocus", unreal_window_handle])
keyDown('alt')
press('p')
keyUp('alt')

sleep(WAIT_BEFORE_CLIENT_START)
run_sub_process(
    ["bash", "run_client.sh"],
    cwd=PATH_TO_HELPER_SCRIPTS
)
