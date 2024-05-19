from machine import Pin,PWM
import utime

Trig=Pin(3,Pin.OUT)
Echo=Pin(2,Pin.IN)
#Setting the LED pin to simulate an analogue output using PWM
LED=PWM(Pin(26))
LED.freq(1000)
LED.duty_u16(0)
#Calibrating the maximum distance your sensor can measure, this value will change depending on your sensor.
max_Ultrasonic_distance_cm=400
#Raspberry Pi Pico has a PMW duty cycle ranging from 0-65025
max_12bit_value=65025;

def read_distance():
    #Sending a pulse
    Trig.value(0)
    utime.sleep_us(2)
    Trig.value(1)
    utime.sleep_us(5)
    Trig.value(0)
    
    #time between pulse release and its arrival as an echo.
    while Echo.value()==0:
        travel_time=utime.ticks_us()
    #time during which the echo is detected     
    while Echo.value()==1:
        pulse_received_time=utime.ticks_us()
    
    timeTaken=pulse_received_time-travel_time
    distance=((0.0343*timeTaken)/2) 
    print("The distance object is ",distance," cm away")
    
    #To prevent brightness values being higher than 3.3 volts
    if distance>max_Ultrasonic_distance_cm:
        distance=max_Ultrasonic_distance_cm
    #Make the brightness value directly proportional to distance of object
    #Also mapping the distance value to an analogue value(0-65025)
    brightness=(max_12bit_value/max_Ultrasonic_distance_cm)*distance
    LED.duty_u16(int(brightness))

while True:
    read_distance()
    utime.sleep(0.5)
