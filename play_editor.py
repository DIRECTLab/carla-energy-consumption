# import unreal
# level_editor_subsystem.editor_request_begin_play()


# unreal.LevelEditorSubsystem().editor_play_simulate()


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

TIME_TO_WAIT = 20
PATH_TO_UI_IMAGE = "carla-play-btn.png"
IMAGE_CONFIDENCE = 0.8

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
        print(
            "TEST unreal_window_handle_bytes: ", 
            unreal_window_handle_bytes
        )
        unreal_window_handle = unreal_window_handle_bytes.split()[0]
        # print("TEST unreal window handle: ", unreal_window_handle)
    except CalledProcessError:
        print("Window not found yet")
        sleep(10)


image_found = False
while not image_found:
    try: 
        result = locateOnScreen(image=PATH_TO_UI_IMAGE, confidence=IMAGE_CONFIDENCE)
        print("Result: ", result)
        image_found = True
    except ImageNotFoundException:
        print("Waiting to load...")
        sleep(5)



# unreal_window_handle_bytes = check_output(
#     ["xdotool", "search", "--name", "Unreal Editor"]
# ) 
# print(
#     "TEST unreal_window_handle_bytes: ", 
#     unreal_window_handle_bytes
# )
# unreal_window_handle = unreal_window_handle_bytes.split()[0]
# print("TEST unreal window handle: ", unreal_window_handle)

run_sub_process(["xdotool", "windowactivate", unreal_window_handle])

keyDown('alt')
press('p')
keyUp('alt')

sleep(TIME_TO_WAIT)

run_sub_process(["bash", "run_carla_demo.sh"])