from paho.mqtt.client import Client

TEMP = "temperature"
HUMIDITY = "humidity"

def on_message(mqttc, userdata, msg):
	print (f"message:{msg.topic}:{msg.payload}:{userdata}")
	if userdata["status"] == 0:
		temp = int(msg.payload) 
		if temp>userdata["temp_threshold"]:
			print(f"Threshold passed {temp}, suscribing to humidity")
			mqttc.subscribe(HUMIDITY)
			userdata["status"] = 1
	elif userdata["status"] == 1:
		if msg.topic==HUMIDITY:
			humidity = int(msg.payload)
			if humidity>userdata["humidity_threshold"]:
				print(f"Humidity Threshold {humidity} passed, cancelling suscription")
				mqttc.unsubscribe(HUMIDITY) 
				userdata["status"] = 0
	elif TEMP in msg.topic:
		temp = int(msg.payload)
		if temp<=userdata["temp_threshold"]:
			print(f"Temperature {temp} under threshold, cancelling suscription")
			userdata["status"]=0
			mqttc.unsubscribe(HUMIDITY)

def on_log(mqttc, data, level, buf, msg):
	print(f"LOG: {data}:{msg}")

def main(broker):
	data = {"temp_threshold":25, "humidity_threshold": 50, "status": 0}
	mqttc = Client(userdata=data)
	mqttc.on_message = on_message
	mqttc.enable_logger()

	mqttc.connect(broker)
	mqttc.subscribe(f"{TEMP}/t1")
	mqttc.loop_forever()

if __name__ == "__main__":
	import sys
	if len(sys.argv)<2:
		print(f"Usage: {sys.argv[0]} broker")
		sys.exit(1)
	broker = sys.argv[1]
	main(broker)