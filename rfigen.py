import serial
import time
import random
import threading

# Open the virtual COM port for writing (e.g., COM6)
ser_write = serial.Serial('COM9', 9600, timeout=1)

# Create a lock for thread-safe serial writing
serial_lock = threading.Lock()

# Simulate 10 RFID tags
rfid_tags = [
    "E2000017221101191890D6A2",
    "E2000017221101191890D6A3",
    "E2000017221101191890D6A4",
    "E2000017221101191890D6A5",
    "E2000017221101191890D6A6",
    "E2000017221101191890D6A7",
    "E2000017221101191890D6A8",
    "E2000017221101191890D6A9",
    "E2000017221101191890D6AA",
    "E2000017221101191890D6AB"
]

def generate_rfid_data(tag):
    """Simulate the reading of an RFID tag for race car laps."""
    while True:
        # Simulate a delay between tag reads (40 seconds to 1 minute 30 seconds)
        delay = random.uniform(40, 90)
        time.sleep(delay)

        # Print the tag and delay to console (for debugging)
        print(f"Read RFID Tag: {tag} after {delay:.2f} seconds")

        # Send the RFID tag to the serial port
        with serial_lock:
            ser_write.write(f"{tag}\n".encode('utf-8'))

def start_simulation():
    """Start the RFID simulation for all tags."""
    threads = []
    for tag in rfid_tags:
        thread = threading.Thread(target=generate_rfid_data, args=(tag,))
        threads.append(thread)
        thread.start()
    
    # Keep the main thread alive to allow background threads to run
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        start_simulation()
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        ser_write.close()
