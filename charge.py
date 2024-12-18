from INA219 import INA219

ina219 = INA219(addr=0x42)


def get_charge_percentage():
    bus_voltage = ina219.getBusVoltage_V()  # voltage on V- (load side)
    p = (bus_voltage - 6) / 2.4 * 100
    if p > 100:
        p = 100
    if p < 0:
        p = 0
    return int(p)


def is_charging():
    current = ina219.getCurrent_mA()  # current in mA
    return current > 0
