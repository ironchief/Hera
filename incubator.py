import time, string, urllib2, subprocess, re
import RPi.GPIO as io

from time import strftime
from lcdproc.server import Server
io.setmode(io.BCM)

def main():
    # pin setup
    temp_pin = 4
    door_pin = 23
    io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

    # lcd setup
    lcd = Server("127.0.0.1", debug=False)
    lcd.start_session()

    screen1 = lcd.add_screen("Screen1")
    screen1.set_heartbeat("off")
    screen1.set_duration(5)

    # lcd strings
    door_status = "shut"
    temperature = "37"+chr(223)+"C"
    humidity = "80% RH"
    network = "wifi"

    # lcd widgets
    display_temperature = screen1.add_string_widget("MyTempWidget", text=temperature, x=1, y=1)
    display_humidity = screen1.add_string_widget("MyHumiWidget", text=humidity, x=1, y=2)
    display_network = screen1.add_string_widget("MyNetworkWidget", text=network, x=10, y=1)
    display_alarm = screen1.add_string_widget("MyStringWidget", text=door_status, x=13, y=2)

    while True:
        # get door status
        if io.input(door_pin):
            door_status = "open"
        else:
            door_status = "shut"

        # get temperature and humidity status
        # output = subprocess.check_output(["./Adafruit_DHT", "2302", str(temp_pin)]);
        # matches_temp = re.search("Temp =\s+([0-9.]+)", output)
        # matches_hum = re.search("Hum =\s+([0-9.]+)", output)
        # if matches_temp and matches_hum:
        #     temperature = float(matches_temp.group(1))
        #     humidity = float(matches_hum.group(1))
        #     display_temperature.set_text(str(temp)+chr(223)+"C")
        #     display_humidity.set_text(str(humidity)+"% RH")
        # Append the data in the spreadsheet, including a timestamp
        # get network status

        if internet_on():
            network = "   wifi"
        else:
            network = "no wifi"
      
        display_network.set_text(network)
        display_alarm.set_text(door_status)
        time.sleep(3)

def internet_on():
    try:
        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

if __name__ == "__main__":
    main()