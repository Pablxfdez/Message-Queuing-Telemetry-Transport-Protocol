from paho.mqtt.client import Client
from time import sleep
import sys


import math
def is_prime(n):
  for i in range(2,int(math.sqrt(n))+1):
    if (n%i) == 0:
      return False
  return True


def on_message_numbers(mqttc, userdata, msg):
    """
    Primer cliente se suscribe si y solo recibe un numero primo
    """
    if float(msg.payload).is_integer() and is_prime(int(msg.payload)):
        print(f' Alarm set for {msg.payload} "')
        mqttc.publish("Timer", f"{msg.payload} -> temp1.")


def on_message_timer(mqttc, userdata, msg):
    """ 
    Espera a la alarma y luego publica en el topic temp1
    """
    data = msg.payload.decode().split(';')
    if len(data) == 3:
        sleep(int(data[0]))
        mqttc.publish(data[1], data[2])


def on_message_temp1(mqttc, userdata, msg):
    # Mismo proceso que en 4_humidity.py
	print (f"message:{msg.topic}:{msg.payload}:{userdata}")
	if userdata["status"] == 0:
		temp = int(msg.payload) 
		if temp>userdata["temp_threshold"]:
			print(f"Threshold passed {temp}, suscribing to humidity")
			mqttc.subscribe("humidity")
			userdata["status"] = 1
	elif userdata["status"] == 1:
		if msg.topic=="humidity":
			humidity = int(msg.payload)
			if humidity>userdata["humidity_threshold"]:
				print(f"Humidity Threshold {humidity} passed, cancelling suscription")
				mqttc.unsubscribe("humidity") 
				userdata["status"] = 0
	elif "temperature" in msg.topic:
		temp = int(msg.payload)
		if temp<=userdata["temp_threshold"]:
			print(f"Temperature {temp} under threshold, cancelling suscription")
			userdata["status"]=0
			mqttc.unsubscribe("humidity")

def main(hostname):
    data = {"temp_threshold":25, "humidity_threshold": 50, "status": 0}
    client_numbers = Client()
    client_numbers.on_message = on_message_numbers # Se conecta a "numbers"
    client_numbers.connect(hostname)
    client_numbers.subscribe("numbers")
    client_numbers.loop_start()

   
    client_timer = Client() 
    client_timer.on_message = on_message_timer   # Se conecta a "timer"
    client_timer.connect(hostname)
    client_timer.subscribe("timer")
    client_timer.loop_start()

  
    client_temp1 = Client(userdata = data)
    client_temp1.on_message = on_message_temp1   # Se conecta a "temp1" 
    client_temp1.connect(hostname)
    client_temp1.subscribe("temp1")
    client_temp1.loop_forever()

if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)