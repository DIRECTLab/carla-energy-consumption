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

EXPECTED_TIME_UNTIL_WINDOW_APPEARANCE = 15
PATH_TO_UI_IMAGE = "carlaUE4-play-btn.png"
IMAGE_CONFIDENCE = 0.8
WAIT_BEFORE_CLIENT_START = 10

Popen(
    ["bash", "start_carla_server.sh"],
    stdout=DEVNULL, 
    stderr=DEVNULL
)

unreal_window_handle = None
while unreal_window_handle is None:
    try:
        unreal_window_handle_bytes = check_output(
            ["xdotool", "search", "--name", "Unreal Editor"]
        ) 
        unreal_window_handle = unreal_window_handle_bytes.split()[0]
    except CalledProcessError:
        sleep(EXPECTED_TIME_UNTIL_WINDOW_APPEARANCE)


image_found = False
while not image_found:
    try: 
        image_found = locateOnScreen(image=PATH_TO_UI_IMAGE, confidence=IMAGE_CONFIDENCE)
    except ImageNotFoundException:
        print("Waiting to load...")
        sleep(5)

run_sub_process(["xdotool", "windowactivate", unreal_window_handle])
keyDown('alt')
press('p')
keyUp('alt')

sleep(WAIT_BEFORE_CLIENT_START)
run_sub_process(["bash", "run_carla_demo.sh"])
