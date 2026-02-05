#!/usr/bin/env python3
import time
import random
from pyModbusTCP.client import ModbusClient

def print_banner():
    """Display ASCII art banner"""
    banner = """
                      __   __                        __      
 /'\_/`\             /\ \ /\ \                      /\ \__   
/\      \     ___    \_\ \\ \ \____   __  __    ____\ \ ,_\  
\ \ \__\ \   / _`\  /'_` \\ \ '__`\\ /\ \/\ \  /',__\\ \ \/  
 \ \ \_/\ \/\ \L\ \/\ \L\ \\ \ \L\ \\ \ \_\ \/\__, `\\ \ \_ 
  \ \_\\ \_\\ \____/\ \___,_\\ \_,__/ \ \____/\ /\____/ \ \__\\
   \/_/ \/_/ \/___/  \/__,_ / \/___/   \/___/  \/___/   \/__/ 
"""
    print(banner)

def int_input(prompt, default):
    """Prompt for an integer with a default; re-prompt on invalid input."""
    while True:
        v = input(prompt).strip()
        if not v:
            return default
        try:
            return int(v)
        except ValueError:
            print("Please enter a valid integer.")


def get_user_inputs():
    """Get configuration from user input with validation"""
    print("=== Modbus TCP Client Configuration ===\n")

    # Get HOST (required, no default)
    HOST = input("Enter Modbus server IP address: ").strip()
    while not HOST:
        print("Error: IP address is required!")
        HOST = input("Enter Modbus server IP address: ").strip()

    # Get PORT
    PORT = int_input("Enter port number [default: 502]: ", 502)

    # Get UNIT_ID
    UNIT_ID = int_input("Enter unit ID [default: 1]: ", 1)

    # Get READ_ADDRESS
    READ_ADDRESS = int_input("Enter read address [default: 100]: ", 100)

    # Get READ_COUNT
    READ_COUNT = int_input("Enter number of registers to read [default: 8]: ", 8)

    # Get WRITE_ADDRESS
    WRITE_ADDRESS = int_input("Enter write address [default: 100]: ", 100)

    # Get WRITE_COUNT
    WRITE_COUNT = int_input("Enter number of registers to write [default: 8]: ", 8)

    print("\n=== Configuration Summary ===")
    print(f"Host: {HOST}")
    print(f"Port: {PORT}")
    print(f"Unit ID: {UNIT_ID}")
    print(f"Read Address: {READ_ADDRESS}")
    print(f"Read Count: {READ_COUNT}")
    print(f"Write Address: {WRITE_ADDRESS}")
    print(f"Write Count: {WRITE_COUNT}")
    print("=" * 30 + "\n")

    return HOST, PORT, UNIT_ID, READ_ADDRESS, READ_COUNT, WRITE_ADDRESS, WRITE_COUNT

def main():
    # Display banner
    print_banner()

    # Get user inputs
    HOST, PORT, UNIT_ID, READ_ADDRESS, READ_COUNT, WRITE_ADDRESS, WRITE_COUNT = get_user_inputs()

    # Open TCP connection (do not auto-open to control retries)
    c = ModbusClient(host=HOST, port=PORT, unit_id=UNIT_ID, auto_open=False)

    try:
        c.open()
    except Exception as e:
        print(f"Failed to open connection: {e}")

    # loop requests to keep connection open
    while True:
        try:
            if not c.is_open():
                print("Connection closed, attempting to open...")
                try:
                    c.open()
                except Exception as e:
                    print(f"Reopen failed: {e}")
                    time.sleep(2)
                    continue

            # Generate random values (0..65535 are valid 16-bit register values)
            random_values = [random.randint(0, 65535) for _ in range(WRITE_COUNT)]

            # read holding registers
            regs = c.read_holding_registers(READ_ADDRESS, READ_COUNT)
            # print holding registers
            if regs is not None:
                print(regs)
            else:
                print("read error")

            # write registers
            success = c.write_multiple_registers(WRITE_ADDRESS, random_values)
            if success:
                print("write ok")
            else:
                print("write error")

            # wait 2s to start again
            time.sleep(2)

        except KeyboardInterrupt:
            print("Interrupted by user, closing connection.")
            try:
                c.close()
            except Exception:
                pass
            break
        except Exception as e:
            print(f"Error during Modbus operation: {e}")
            # back off a bit before retrying
            time.sleep(2)


if __name__ == "__main__":
    main()