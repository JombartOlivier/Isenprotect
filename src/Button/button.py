#!/usr/bin/env python3 
#coding : utf8

import RPi.GPIO as GPIO  
import time 
import pygame
import os



#assigment GPIO
led=18
button=25
#setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT) 							       #led du bouton
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (button)

#init lecteur audio
pygame.mixer.init()
pygame.mixer.music.set_volume(2.0)

path = "/home/pi/Documents/Isenprotect/src/fichiers_audio/Alerte_collision_detectee.mp3"
path2 = "/home/pi/Documents/Isenprotect/src/fichiers_audio/Envoie_des_secours_a_votre_position.mp3"										
path3 = "/home/pi/Documents/Isenprotect/src/fichiers_audio/Fin_d_alerte.mp3"		


class Button :

	def __init__(self) :

		self.state=0
		self.timing=0

	# def _set_state(self,state) :
	# 	self.state=state

	# def _set_timing(self,timing):
	# 	self.timing=timing

	# def _get_state(self):
	# 	print(self.state)
	# 	return self.state

	# def _get_timing(self):
	# 	print(self.timing)
	#	return self.timing
	def _get_timing(self):
		print(self.timing)
		return self.timing


	def playAudio():
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			continue

	def my_callback(self,timing,state):
		self.timing=timing
		self.state=state
		print("coucou")
		timing=10
		state=1
	
	

	def detectionButton(self,timing,state):
		GPIO.add_event_detect(button, GPIO.RISING, callback=my_callback(self,0,0))
		self.timing=timing
		self.state=state
		while timing < 10 :
			GPIO.output(led,GPIO.HIGH)   #led clignote 
			pygame.mixer.music.load(path)
			print("Alerte, collision detectee, attente de confirmation")
			Button.playAudio()
			GPIO.output(led,GPIO.LOW)
			print(timing)
			time.sleep(0.5)
			self.timing=timing
			timing+=1


		if state==0:
			print("accident confirme, envoie des secours à votre position")
			pygame.mixer.music.load(path2)
			Button.playAudio()

		else :	
			print("fin de l'alerte")
			pygame.mixer.music.load(path3)
			Button.playAudio()

		
