###import RPi.GPIO as GPIO
import socket
import time
import datetime
#print("rechercher des appareils BLT")
#nearby_divices=discover_devices(lookup_names = True)

#print("found %d devices" % len(nearby_devices))


#for j in nearby_devices:
 #   if j =="D3:9F:17:DB:B1:3F":
  #      print("Ok_adr_MAC")

client_socket=socket.socket(socket.AF_BLUETOOTH,socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client_socket.connect(("24:A1:60:53:C1:2A",1))
#time.sleep(50)
size = 1024
k=100

for i in range (0,k):
    HeatBeat=client_socket.recv(size).decode("utf-8")
    print(HeatBeat)
   
    date=datetime.datetime.now()
    date = str(date)
    f= open('data.txt', 'a')
    f.write("Date;Hour;Minute;Second;HeatBeat;\n")
    f.write(date)
    f.write(";")
    f.write(HeatBeat)
    f.write('\n')
f.close()

client_socket.close()