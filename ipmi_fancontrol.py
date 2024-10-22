#!/usr/bin/env python3

import argparse
import pyipmi
import pyipmi.interfaces
import numpy as np
from scipy.interpolate import interp1d
from time import sleep

#### CONFIG ####

# Get IDs using ipmitool.py -I ipmitool -o interface_type=open sdr list
cpu_temps = (0x133, 0x134)
fan_banks = 2
sleep_sec = 3

fan_curve = { # Temprature: Fan-Speed
        30: 0, 
        40: 10, 
        50: 20, 
        55: 50, 
        60: 75, 
        70: 85,
        80: 100
    }

verbose = 1

###########

def get_cpu_temperature(ipmic):
    temperature = -1
    used_id = -1
    for sensor_id in cpu_temps:
        try:
            sens_temperature = ipmic.get_sensor_reading(sensor_id)[0]
            if verbose >= 4:
                print(f"Sensor {sensor_id} reported {sens_temperature}")
            if sens_temperature > temperature:
                temperature = sens_temperature
                used_id = sensor_id
        except:
            if verbose >= 1:
                print(f"Failed to read sensor {sensor_id}")

    if verbose >= 3:
        print(f"Using Temperature {temperature} from sensor {used_id}")

    return temperature

def generate_fan_curve(fan_curve):
    x = np.array(sorted(fan_curve.keys()))
    y = np.array([fan_curve[key] for key in x])

    f = interp1d(x, y, kind='cubic', fill_value=(min(y), max(y)), bounds_error=False)
    return f

def get_fan_target_speed(fan_intp, temperature, last_speed=-1):
    fan_speed = float(fan_intp(temperature))
    fan_speed_hex = int((fan_speed / 100) * 0xFF)
    if verbose >= 3:
        print(f"Target fan speed is now {fan_speed:.0f}% (0x{fan_speed_hex:02x}) for peak temperature {temperature}°C")
    elif verbose >= 1 and last_speed != fan_speed_hex:
        print(f"Target fan speed changed to {fan_speed:.0f}% (0x{fan_speed_hex:02x}) for peak temperature {temperature}°C")
    return fan_speed_hex

def set_fan_speed(ipmic, speed):
    for bank in range(1, fan_banks+1):
        if verbose >= 4:
            print(f"Setting Bank {bank} to 0x{speed:02x}")
        ipmic.raw_command(0, 0x3a, (0x07, bank, speed, 0x01))

ipmii = pyipmi.interfaces.create_interface('ipmitool', interface_type='open')
ipmic = pyipmi.create_connection(ipmii)
ipmic.session.establish()

fan_intp = generate_fan_curve(fan_curve)

last_speed = 0
while True:
    temperature = get_cpu_temperature(ipmic)
    fan_speed = get_fan_target_speed(fan_intp, temperature, last_speed)
    set_fan_speed(ipmic, fan_speed)
    last_speed = fan_speed

    sleep(sleep_sec)