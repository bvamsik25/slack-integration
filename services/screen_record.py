import os
import time
import subprocess
import requests
import certifi
from PIL import Image

import config

ADB_SCREENSHOT_PATH = "/sdcard/screenshot.png"
LOCAL_SCREENSHOT_DIR = "screenshots"
GIF_OUTPUT_PATH = "screenshots/output.gif"


def run_command(*cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip(), result.stderr.strip()


def reset_adb():
    """Restart ADB to ensure the emulator is connected properly."""
    print("Restarting ADB...")
    run_command("adb", "kill-server")
    run_command("adb", "start-server")
    run_command("adb", "devices")
    print("ADB restarted.")


def capture_screenshot(local_filename):
    """Capture a screenshot and save it locally."""
    print("Taking screenshot...")

    # Take a screenshot on the emulator/device
    run_command("adb", "shell", "screencap", "-p", ADB_SCREENSHOT_PATH)

    # Pull the screenshot to the local machine
    stdout, stderr = run_command("adb", "pull", ADB_SCREENSHOT_PATH, local_filename)

    if "does not exist" in stderr:
        print("Error: Screenshot file not found on emulator.")
        return False

    print(f"Screenshot saved: {local_filename}")
    return True


def capture_multiple_screenshots(num_screenshots=30, interval=1):
    """Capture multiple screenshots at defined intervals."""
    if not os.path.exists(LOCAL_SCREENSHOT_DIR):
        os.makedirs(LOCAL_SCREENSHOT_DIR)

    screenshot_files = []

    for i in range(num_screenshots):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        local_filename = os.path.join(LOCAL_SCREENSHOT_DIR, f"screenshot_{timestamp}.png")

        success = capture_screenshot(local_filename)
        if not success:
            break  # Stop capturing if there is an error

        screenshot_files.append(local_filename)

        if i < num_screenshots - 1:
            time.sleep(interval)  # Wait before taking the next screenshot

    return screenshot_files


def create_gif(image_files, output_path, duration=500):
    """Convert a sequence of images into a GIF."""
    if not image_files:
        print("No screenshots to create a GIF.")
        return False

    images = [Image.open(img) for img in image_files]
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)

    print(f"GIF created: {output_path}")
    return True


def upload_to_imgbb():
    with open(GIF_OUTPUT_PATH, "rb") as file:
        response = requests.post(
            config.IMBB_URL,
            files={"image": file},
            verify=certifi.where()
        )

        if response.status_code == 200:
            response_data = response.json()
            config.IMAGE_URL = response_data["data"]["url"]
        else:
            print("Upload failed:", response.text)
            config.IMAGE_URL = None

