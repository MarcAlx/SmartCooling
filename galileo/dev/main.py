# -*- coding: utf-8 -*-

from threading import Thread
from time import sleep
import paho.mqtt.client as mqtt
import lib.GPIO_Intel as GPIO

"""
    author : Developed by Marc-Alexandre Blanchard && Morgan Chaboud
    date : 2015
"""

class Application(object):
	""" 
		Application class 
		IO10 : 0 -> fan on
		IO10 : 1 -> fan off
		IO11 : 0 -> 5V
		IO11 : 1 -> 9V
	"""
	_NAME,_VERSION,_REFRESH_TIME="M2M",1.0,1
	
	_BROKER_URL = "192.168.1.1"
	_BROKER_PORT = 1883
	_KEEP_ALIVE = 60
	_TOPIC = ['/fan']
	_FAN_STATE_PIN = 'IO10'
	_FAN_SPEED_PIN = 'IO11'
	
	_client = mqtt.Client()

	_GPIO = GPIO.Intel()

	def __init__(self):
		print "--- initialisation"
		self._GPIO.setup(self._FAN_STATE_PIN)
		self._GPIO.setup(self._FAN_SPEED_PIN)
		#stop fan
		self._GPIO.output(self._FAN_STATE_PIN,1)
		#set minimal fan speed
		self._GPIO.output(self._FAN_SPEED_PIN,1)
		
	def on_connect(self,client,userdata,flags,rc):
		print "--- connected with result code "+str(rc)
		for topic in self._TOPIC:
			self.subscribe(topic)

	def activate_fan(self,lvl):
		#write to correct pin according to level
		if(lvl == 1):
			self._GPIO.output(self._FAN_STATE_PIN,'0')
			self._GPIO.output(self._FAN_SPEED_PIN,'1')
		elif(lvl == 2):
			self._GPIO.output(self._FAN_STATE_PIN,'0')
			self._GPIO.output(self._FAN_SPEED_PIN,'0')
		print "--- fan_activated"

	def deactivate_fan(self):
		self._GPIO.output(self._FAN_STATE_PIN,'1')
		self._GPIO.output(self._FAN_SPEED_PIN,'1')		
		print "--- fan_deactivated"

	def on_message(self,client, userdata, msg):
		print("--- on_message : topic : "+msg.topic+" content : "+str(msg.payload))
		if(msg.topic=="/fan"):
			if(str(msg.payload)=="0"):
				self.deactivate_fan()
			elif(str(msg.payload)=="1"):
				self.activate_fan(1) 
			elif(str(msg.payload)=="2"):
				self.activate_fan(2) 
			else:
				print "--- on_message : unrecognized command"

	def publish(self,topic,message):
		print "--- publish on "+topic+" : "+message
		self._client.publish(topic,message)

	def subscribe(self,topic):
		print "--- subscribing to \'"+topic+"\'"
		self._client.subscribe(topic)

	def mainloop(self):
		#initiate
		self._client.connect(self._BROKER_URL,self._BROKER_PORT,self._KEEP_ALIVE)
		self._client.on_connect = self.on_connect
		self._client.on_message = self.on_message

		#Threading
		#Create threads
		#client
		self._client.loop_forever()

if __name__ == '__main__':
	print "--- launching - crl-z to quit "
	Application().mainloop()
