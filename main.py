import time
import machine

led = machine.Pin("LED",machine.Pin.OUT)

def main():
    while 1:
        led.on()
        time.sleep_ms(500)
        led.off()
        time.sleep_ms(500)

if __name__ == "__main__":
    main()
