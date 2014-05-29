# Hera
### Laboratory Incubator Data Logger
Log data from your incubator to Google Docs and view stats on your LCD.

Feature:
- View stats in real time on your lcd
- Log data straight to Google Docs
- Easily embed real time data on the web

## Hardware
- Raspberry Pi
- Temperature/humidity sensor (DHT11,DHT22, AM2302) see [Adafruit](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging?view=all)
- LCD USB screen see [Adafruit](https://learn.adafruit.com/usb-plus-serial-backpack?view=all)
- Magnetic Door sensor see [Adafruit](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-12-sensing-movement?view=all)

## Install
Download this repo to a folder on your raspberry pi
```
git clone git://github.com/ironchief/Hera.git
```
Download Adafruit Raspberry Pi Python code + DHT library
```
git clone git://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
```
Install LCDProc to control the USB LCD
```
$ sudo apt-get install -y lcdproc
```
Install the python dependencies
```
$ pip install -r requirements.txt
```
Enter your Google username and password into environment.py
```
email       = 'email@gmail.com'
password    = 'password'
spreadsheet = 'worksheet'
```
Run incubator.py
```
sudo python incubator.py
```

## Example
![lcd](https://raw.github.com/ironchief/Hera/master/lcd.png "")