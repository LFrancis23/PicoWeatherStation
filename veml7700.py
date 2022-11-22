import time
def veml7700_read(veml7700,i2c2):
    lux = bytearray(2)
    addr = veml7700[0]
    als = veml7700[1]
    gain = 1.8432
    time.sleep(.04)
    i2c2.readfrom_mem_into(addr,als,lux)
    lux = lux[0]+lux[1]*256
    lux = lux*gain
    return lux

def veml7700_init(i2c2):
    
    addr = const(0x10)
    als_conf_0 = const(0x00)
    als_WH = const(0x01)
    als_WL = const(0x02)
    pow_sav = const(0x03)

    als = const(0x04)
    white = const(0x05)
    interrupt = const(0x06)

    confValues = bytearray([0x00, 0x13])

    interrupt_high = bytearray([0x00,0x00])

    interrupt_low = bytearray([0x00,0x00])

    power_save_mode = bytearray([0x00,0x00])

    i2c2.writeto_mem(0x10,0x00,bytearray([0x00, 0x13]))
    i2c2.writeto_mem(addr,als_WH, interrupt_high)
    i2c2.writeto_mem(addr,als_WL, interrupt_low)
    i2c2.writeto_mem(addr, pow_sav, power_save_mode)
    return [addr,als]