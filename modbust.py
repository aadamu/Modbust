#!/usr/bin/env python3
import time
import random
import sys
from pyModbusTCP.client import ModbusClient

def main():
    # Configuration
    HOST = "10.150.203.193"
    PORT = 502
    UNIT_ID = 1
    READ_ADDRESS = 50
    READ_COUNT = 8
    WRITE_ADDRESS = 100
    
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
            random_values = [random.randint(1, 999) for _ in range(8)]
            
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
