import json
import os
import atexit
import threading
import time

PROCESSED_EVENTS_FILE = "processed_events.json"


# Load existing processed events from file
def load_processed_events():
    if os.path.exists(PROCESSED_EVENTS_FILE):
        try:
            with open(PROCESSED_EVENTS_FILE, "r") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print("Error loading processed events file. Resetting.")
            return set()
    return set()


# Save processed events to file
def save_processed_events():
    with open(PROCESSED_EVENTS_FILE, "w") as f:
        json.dump(list(processed_events), f)


# Periodically clear the processed events
def periodic_clear():
    while True:
        time.sleep(3600)  # Clear every 1 hour
        print("Clearing processed events...")
        processed_events.clear()
        save_processed_events()


# Ensure cleanup happens when the server stops
def cleanup_on_exit():
    print("Server stopping... Cleaning processed events!")
    os.remove(PROCESSED_EVENTS_FILE) if os.path.exists(PROCESSED_EVENTS_FILE) else None


# Register cleanup on exit
atexit.register(cleanup_on_exit)

# Initialize the processed events
processed_events = load_processed_events()

# Start a background thread to periodically clear events
threading.Thread(target=periodic_clear, daemon=True).start()
