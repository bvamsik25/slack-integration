import subprocess
import random
import time


APP_PACKAGE = "com.android.chrome"
APP_ACTIVITY = "com.google.android.apps.chrome.Main"
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920
NUM_ACTIONS = 30
RUNNING = False
MAX_LENGTH = 2990


def get_screen_size():
    """Fetches screen size dynamically."""
    global SCREEN_WIDTH, SCREEN_HEIGHT
    try:
        output = subprocess.check_output(["adb", "shell", "wm", "size"]).decode()
        SCREEN_WIDTH, SCREEN_HEIGHT = map(int, output.split(":")[-1].strip().split("x"))
    except Exception as e:
        print("Failed to get screen size, using default values:", str(e))


def open_app():
    """Launches the specified app."""
    subprocess.run(["adb", "shell", "am", "start", "-n", f"{APP_PACKAGE}/{APP_ACTIVITY}"])
    time.sleep(5)  # Wait for the app to load


def tap_random():
    """Simulates a random tap."""
    x = random.randint(100, SCREEN_WIDTH - 100)
    y = random.randint(200, SCREEN_HEIGHT - 200)

    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])
    time.sleep(random.uniform(0.5, 2))


def swipe_random():
    """Simulates a random swipe."""
    x1 = random.randint(200, SCREEN_WIDTH - 200)
    y1 = random.randint(400, SCREEN_HEIGHT - 400)
    x2 = x1 + random.randint(-200, 200)
    y2 = y1 + random.randint(-500, 500)

    subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2)])
    time.sleep(random.uniform(1, 3))


def press_back():
    """Presses the back button."""
    subprocess.run(["adb", "shell", "input", "keyevent", "4"])
    time.sleep(random.uniform(1, 2))


def random_action():
    """Randomly chooses an action."""
    action = random.choice(["tap", "swipe", "back"])
    if action == "tap":
        tap_random()
    elif action == "swipe":
        swipe_random()
    elif action == "back":
        press_back()


def ui_test_loop():
    """Runs the random UI test."""
    global RUNNING
    get_screen_size()
    open_app()

    action_count = 0
    while RUNNING and (NUM_ACTIONS is None or action_count < NUM_ACTIONS):
        random_action()
        action_count += 1

    print("UI Test Stopped!")


def start_ui_test():
    """Starts the UI test synchronously."""
    global RUNNING
    if not RUNNING:
        print("Starting UI Test...")
        RUNNING = True
        ui_test_loop()
    else:
        print("UI Test is already running!")


def stop_ui_test():
    """Stops the UI test."""
    global RUNNING
    if RUNNING:
        print("Stopping UI Test...")
        RUNNING = False
    else:
        print("UI Test is not running!")


def get_emulator_logs():
    """Fetches emulator logs."""
    try:
        process = subprocess.run(
            ["adb", "logcat", "-d", "-t", "10"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        emulator_logs = process.stdout.strip()
        truncated_logs = emulator_logs[:MAX_LENGTH] + "..." if len(emulator_logs) > MAX_LENGTH else emulator_logs
        log_chunks = [truncated_logs[i:i + 2900] for i in range(0, len(truncated_logs), MAX_LENGTH)]
        return log_chunks if emulator_logs else "No logs available."
    except Exception as e:
        print("Error fetching logs:", str(e))
        return "No logs available."
