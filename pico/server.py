from connection import PASSWORD, PORT, SSID
import network
import socket
from machine import Pin
import utime
import rp2
import sys
import json

pico_led = Pin("LED", Pin.OUT)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        pico_led.on()
        utime.sleep(0.5)
        pico_led.off()
        utime.sleep(0.5)
    
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    pico_led.on()
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, PORT)
    sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    return sock
    
def serve(connection, get_data):
    #Start a web server
    while True:
        client = connection.accept()[0]

        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        client.send('HTTP/1.0 200 OK\r\n')
        client.send("Content-Type: application/json; charset=utf-8\r\n\r\n")
        
        data = {}
        if request == '/data':
            data = get_data()

        json_str = json.dumps(data)
        client.send(json_str.encode())

        client.close()
