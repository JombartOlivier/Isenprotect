#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Test de la phase après detection crash
import RPi.GPIO as GPIO
import time
import pygame
import pygame

#init lecteur audio
pygame.mixer.init()
pygame.mixer.music.set_volume(2.0)

#flag de sortie de boucle
valeur=0
accident_potentiel=0

#setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) 							  #LED du bouton
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    #detection enclenchement bouton


#fonction play music
def play_music() :

	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
   		continue

#Si accident, on attend __s

while accident_potentiel<10 :
	GPIO.output(18,GPIO.HIGH)
	print("Alerte, collision detectee, attente de confirmation")	
	bouton=GPIO.input(4)
	print(bouton)
	pygame.mixer.music.load("Alerte_collision_detectee.wav")
	play_music()

	if bouton==1: #Si le bouton est enclenché
		print("accident non confirme")
		pygame.mixer.music.load("Fin_d_alerte.wav")
		play_music()
		accident_potentiel=15
		valeur=1

	accident_potentiel+=1
	GPIO.output(18,GPIO.LOW)
	time.sleep(0.5)

if valeur==0:
	print("accident confirme, envoie des secours à votre position")
	pygame.mixer.music.load("Envoie_des_secours_ a_votre_position.wav")
	play_music()


