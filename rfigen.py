import serial
import time
import random
import threading

def get_com_port():
    """Prompt the user to enter the COM port."""
    while True:
        com_port = input("Enter the COM port (e.g., COM9): ")
        try:
            # Attempt to open the specified COM port
            ser = serial.Serial(com_port, 9600, timeout=1)
            ser.close()  # Close the port immediately if successful
            return com_port
        except serial.SerialException as e:
            print(f"Error: Could not open port {com_port}. Please try again. ({e})")

def get_time_interval():
    """Prompt the user to enter the minimum and maximum delay times."""
    while True:
        try:
            min_time = float(input("Enter the minimum delay time (in seconds): "))
            max_time = float(input("Enter the maximum delay time (in seconds): "))
            if min_time > 0 and max_time > min_time:
                return min_time, max_time
            else:
                print("Please ensure the minimum time is positive and the maximum time is greater than the minimum time.")
        except ValueError:
            print("Invalid input. Please enter numeric values.")

def get_number_of_tags():
    """Prompt the user to enter the number of RFID tags to simulate."""
    while True:
        try:
            num_tags = int(input("Enter the number of RFID tags to simulate (up to 10): "))
            if 1 <= num_tags <= 10:
                return num_tags
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def send_custom_data():
    """Allow the user to send custom data manually."""
    while True:
        custom_data = input("Enter the custom data to send (or 'exit' to stop): ")
        if custom_data.lower() == 'exit':
            break
        with serial_lock:
            ser_write.write(f"{custom_data}\n".encode('utf-8'))
            ser_write.flush()
        print(f"Sent custom data: {custom_data}")

def choose_mode():
    """Prompt the user to choose between sending custom data or RFID timing simulation."""
    while True:
        print("Choose mode:")
        print("1. Custom")
        print("2. RFID")
        choice = input("Enter the number corresponding to your choice: ")
        if choice == '1':
            return 'custom'
        elif choice == '2':
            return 'rfid'
        else:
            print("Invalid choice. Please enter either '1' for 'custom' or '2' for 'rfid'.")

# Get the COM port from the user
com_port = get_com_port()

# Open the virtual COM port for writing
ser_write = serial.Serial(com_port, 9600, timeout=1)

# Create a lock for thread-safe serial writing
serial_lock = threading.Lock()

# Custom list of 10 RFID tags
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

# Flag to signal threads to stop
stop_threads = threading.Event()

def generate_rfid_data(tag):
    """Simulate the reading of an RFID tag for race car laps."""
    try:
        # Send the first RFID tag immediately
        print(f"Initial read RFID Tag: {tag}")
        with serial_lock:
            ser_write.write(f"{tag}\n".encode('utf-8'))
            ser_write.flush()  # Ensure the buffer is flushed after each write

        while not stop_threads.is_set():
            try:
                # Simulate a delay between subsequent tag reads
                delay = random.uniform(min_time, max_time)
                # Check stop signal periodically during the delay
                for _ in range(int(delay * 10)):  # Check every 0.1 second
                    if stop_threads.is_set():
                        return
                    time.sleep(0.1)

                # Print the tag and delay to console (for debugging)
                print(f"Read RFID Tag: {tag} after {delay:.2f} seconds")

                # Send the RFID tag to the serial port
                with serial_lock:
                    ser_write.write(f"{tag}\n".encode('utf-8'))
                    ser_write.flush()  # Ensure the buffer is flushed after each write
            except Exception as e:
                print(f"Error with RFID tag {tag}: {e}")
    except Exception as e:
        print(f"Error with initial read RFID tag {tag}: {e}")

def start_simulation():
    """Start the RFID simulation for all tags."""
    print("STARTED waiting for first RFID")
    threads = []
    for tag in selected_tags:
        thread = threading.Thread(target=generate_rfid_data, args=(tag,))
        thread.daemon = True  # Make the thread a daemon thread
        threads.append(thread)
        thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping simulation...")
        stop_threads.set()
        # No need to join daemon threads as they will automatically exit
        ser_write.close()
        print("Simulation stopped.")

if __name__ == "__main__":
    mode = choose_mode()
    if mode == 'custom':
        send_custom_data()
    elif mode == 'rfid':
        min_time, max_time = get_time_interval()
        num_tags = get_number_of_tags()
        selected_tags = rfid_tags[:num_tags]
        start_simulation()
