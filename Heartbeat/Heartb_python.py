import serial  
import http.client as http  
import urllib  

ser = serial.Serial('/dev/ttyACM0',9600)  

key = "17JIT9D83RJSAXTN"  

def upload_to_ts(val):      

    params = urllib.parse.urlencode({'field1': val, 'key':key })   

    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}  

    conn = http.HTTPConnection("api.thingspeak.com:80")  

    try:  

        conn.request("POST", "/update", params, headers)  

        response = conn.getresponse()  

        data = response.read()  

        conn.close()  

    except Exception:  

        print ("Connection failed")  

    except KeyboardInterrupt:  

        print ("\nExiting.....")  

        exit()    

while True:  

    try:  

        read_serial=ser.readline()  

        bpm = read_serial.decode('utf-8').strip()  

        print (bpm)  

        upload_to_ts(bpm)  

    except KeyboardInterrupt:  

        print ("\nExiting.....")  

        break  