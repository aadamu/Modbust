#!/usr/bin/env python3
import time
import random
from pyModbusTCP.client import ModbusClient
modbus_server = input("Enter server IP address: ")
# Open TCP connection
c = ModbusClient(host=modbus_server, port=502, unit_id=1, auto_open=True)
# loop requests to keep connection open
while True:

 # create random numbers
 randint_1 = random.randint(1,999)
 randint_2 = random.randint(1,999)
 randint_3 = random.randint(1,999)
 randint_4 = random.randint(1,999)
 randint_5 = random.randint(1,999)
 randint_6 = random.randint(1,999)
 randint_7 = random.randint(1,999)
 randint_8 = random.randint(1,999)
 # read holding registers
 regs = c.read_holding_registers(50, 8)
 # print holding registers
 if regs:
     print(regs)
 else:
     print("read error")
 # write registers
 if c.write_multiple_registers(100, [randint_1, randint_2, randint_3,  randint_4, randint_5, randint_6, randint_7, randint_8]):
    print("write ok")
 else:
     print("write error")
 # wait 2s to start again
 time.sleep(2)
