#!/usr/bin/env python3
import time
import random
import sys
from pyModbusTCP.client import ModbusClient

def print_banner():
    """Display ASCII art banner"""
    banner = """
                      __   __                        __      
 /'\_/`\             /\ \ /\ \                      /\ \__   
/\      \     ___    \_\ \\ \ \____   __  __    ____\ \ ,_\  
\ \ \__\ \   / _`\  /'_` \\ \ '__`\ /\ \/\ \  /',__\\ \ \/  
 \ \ \_/\ \ /\ \L\ \/\ \L\ \\ \ \L\ \\ \ \_\ \/\__, `\\ \ \_ 
  \ \_\\ \_\\ \____/\ \___,_\\ \_,__/ \ \____/\/\____/ \ \__\\
   \/_/ \/_/ \/___/  \/__,_ / \/___/   \/___/  \/___/   \/__/
"""
    print(banner)

def get_user_inputs():
    """Get configuration from user input with validation"""
    print("=== Modbus TCP Client Configuration ===\n")
    
    # Get HOST (required, no default)
    HOST = input("Enter Modbus server IP address: ").strip()
    while not HOST:
        print("Error: IP address is required!")
        HOST = input("Enter Modbus server IP address: ").strip()
    
    # Get PORT
    port_input = input("Enter port number [default: 502]: ").strip()
    PORT = int(port_input) if port_input else 502
    
    # Get UNIT_ID
    unit_input = input("Enter unit ID [default: 1]: ").strip()
    UNIT_ID = int(unit_input) if unit_input else 1
    
    # Get READ_ADDRESS
    read_addr_input = input("Enter read address [default: 100]: ").strip()
    READ_ADDRESS = int(read_addr_input) if read_addr_input else 100
    
    # Get READ_COUNT
    read_count_input = input("Enter number of registers to read [default: 8]: ").strip()
    READ_COUNT = int(read_count_input) if read_count_input else 8
    
    # Get WRITE_ADDRESS
    write_addr_input = input("Enter write address [default: 100]: ").strip()
    WRITE_ADDRESS = int(write_addr_input) if write_addr_input else 100
    
    print("\n=== Configuration Summary ===")
    print(f"Host: {HOST}")
    print(f"Port: {PORT}")
    print(f"Unit ID: {UNIT_ID}")
    print(f"Read Address: {READ_ADDRESS}")
    print(f"Read Count: {READ_COUNT}")
    print(f"Write Address: {WRITE_ADDRESS}")
    print("=" * 30 + "\n")
    
    return HOST, PORT, UNIT_ID, READ_ADDRESS, READ_COUNT, WRITE_ADDRESS

def main():
    # Get configuration from user
    try:
        HOST, PORT, UNIT_ID, READ_ADDRESS, READ_COUNT, WRITE_ADDRESS = get_user_inputs()
    except ValueError:
        print("Error: Invalid input. Please enter numeric values for port, unit ID, and addresses.")
        sys.exit(1)
    
    # Create client
    client = ModbusClient(host=HOST, port=PORT, unit_id=UNIT_ID, auto_open=True)
    
    # Check connection
    if not client.is_open:
        print(f"Error: Unable to connect to {HOST}:{PORT}")
        sys.exit(1)
    
    print(f"Connected to {HOST}:{PORT}")
    
    try:
        while True:
            # Generate random values
            random_values = [random.randint(1, 999) for _ in range(READ_COUNT)]
            
            # Read holding registers
            regs = client.read_holding_registers(READ_ADDRESS, READ_COUNT)
            if regs:
                print(f"Read: {regs}")
            else:
                print("Read error")
            
            # Write registers
            if client.write_multiple_registers(WRITE_ADDRESS, random_values):
                print(f"Write OK: {random_values}")
            else:
                print("Write error")
            
            # Wait before next iteration
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        client.close()
        print("Connection closed")

if __name__ == "__main__":
    main()
