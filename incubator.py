import time, string, urllib2, subprocess, re, gspread, datetime, environment
import RPi.GPIO as io

from time import strftime
from lcdproc.server import Server
from random import uniform
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
    error = "log err"

    # Account details for google docs
    email       = environment.email
    password    = environment.password
    spreadsheet = environment.spreadsheet

    try:
        # Login with your Google account
        gc = gspread.login(email, password)
        # Open a worksheet from your spreadsheet using the filename
        worksheet = gc.open(spreadsheet).sheet1
    except:
        network_status = error

    # lcd widgets
    display_temperature = screen1.add_string_widget("MyTempWidget", x=1, y=1)
    display_humidity = screen1.add_string_widget("MyHumiWidget", x=1, y=2)
    display_network = screen1.add_string_widget("MyNetworkWidget", x=10, y=1)
    display_alarm = screen1.add_string_widget("MyStringWidget", x=13, y=2)

    while True:
        # get door status
        if io.input(door_pin):
            door_status = "open"
        else:
            door_status = "shut"

        # get temperature and humidity status
        # output = subprocess.check_output(["./Adafruit_DHT", "2302", str(temp_pin)]);
        temp = uniform( 36, 37)
        hum = uniform( 75, 80)
        output = "Temp = %.1f *C, Hum = %.1f %%" % (temp, hum)
        matches_temp = re.search("Temp =\s+([0-9.]+)", output)
        matches_hum = re.search("Hum =\s+([0-9.]+)", output)
        if matches_temp and matches_hum:
            temperature = float(matches_temp.group(1))
            humidity = float(matches_hum.group(1))
            temperature_status = str(temperature)+chr(223)+"C"
            humidity_status = str(humidity)+"% RH"
        else:
            temperature_status = "--.-C"
            humidity_status = "--.-% RH"


        # get network status
        if internet_on():
            network_status = "   wifi"
            if matches_temp and matches_hum:
                try:
                    values = [datetime.datetime.now(), temperature, humidity]
                    worksheet.append_row(values)
                except:
                    network_status = error
        else:
            network_status = "no wifi"
        
        display_temperature.set_text(temperature_status)
        display_humidity.set_text(humidity_status)
        display_network.set_text(network_status)
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