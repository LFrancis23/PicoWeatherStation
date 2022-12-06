#Name: Landyn Francis
#File: veml7700.py
#Purpose: Code to interface with the VEML7700
import time
def veml7700_read(veml7700,i2c2):
    lux = bytearray(2) #Lux returned as 2 bytes
    addr = veml7700[0] 
    als = veml7700[1]
    gain = 1.8432 #Gain for max range, low resolution
    time.sleep(.04)
    i2c2.readfrom_mem_into(addr,als,lux)#Read data from sensor
    lux = lux[0]+lux[1]*256 #Sensor data conversion
    lux = lux*gain #Apply gain
    return lux

def veml7700_init(i2c2):
    
    #Command codes
    addr = const(0x10) #Device address
    als_conf_0 = const(0x00) #Gain, integration time, interrupt, shutdown
    als_WH = const(0x01) #High threshold setting
    als_WL = const(0x02) #Low threshold setting
    pow_sav = const(0x03) #Power save mode 
    als = const(0x04)
    white = const(0x05)
    interrupt = const(0x06)

    #Data sections (mostly default)
    confValues = bytearray([0x00, 0x13]) #ALS shutdown and interrupt enable, persisntence protect number 2, gain set to 1x, applied externally

    interrupt_high = bytearray([0x00,0x00])

    interrupt_low = bytearray([0x00,0x00])

    power_save_mode = bytearray([0x00,0x00])

    #Write to all the configuration registers. 
    i2c2.writeto_mem(addr,als_conf_0,confValues)
    i2c2.writeto_mem(addr,als_WH, interrupt_high)
    i2c2.writeto_mem(addr,als_WL, interrupt_low)
    i2c2.writeto_mem(addr, pow_sav, power_save_mode)
    #Return address and sensor
    return [addr,als]