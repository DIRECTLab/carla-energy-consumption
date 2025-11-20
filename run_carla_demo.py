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
from argparse import ArgumentParser

PATH_TO_HELPER_SCRIPTS = "./demo_helper_scripts"
PATH_TO_UI_IMAGE = "./docs/figures/carlaUE4-play-btn.png"
WINDOW_NAME = "CarlaUE4 - Unreal Editor"

IMAGE_CONFIDENCE = 0.8

EXPECTED_TIME_UNTIL_WINDOW_APPEARANCE = 70
RETRY_WINDOW = 5
WAIT_BEFORE_CLIENT_START = 30

parser = ArgumentParser(description="Parses arguments for the internal client helper bash script.")
parser.add_argument(
    '-a', action='store_true',
    help='Runs the automated simulation demo. Cannot be combined with other options.'
)
parser.add_argument(
    '-v', type=str, default=None, 
    help='Specify name of the vehicle csv to load. Eg. for tesla.csv enter "tesla".'
)
parser.add_argument(
    '-c', type=str, default=None, 
    help='Specify the name of the csv file with the corresponding map\'s chargers'
)
parser.add_argument(
    '-r', type=str, default=None, 
    help='Specify desired resolution for the client screen. Eg. "1920x1080"'
)
parser.add_argument(
    '-d', action='store_true', 
    help='Debug mode. Show all output from client start script.'
)

args_dict = vars(parser.parse_args())


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
command_args = ["bash", "run_client.sh"]
for key, value in args_dict.items():
    if value is True:
        command_args.append(f"-{key}")
    elif value is not None and value is not False:
        command_args.append(f"-{key}")
        print(type(key))
        print(type(value))
        command_args.append(f"{value}")

run_sub_process(
    args=command_args,
    cwd=PATH_TO_HELPER_SCRIPTS
)
