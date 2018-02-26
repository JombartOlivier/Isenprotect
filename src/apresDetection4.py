#!/usr/bin/env python3 
#coding : utf8
  
import RPi.GPIO as GPIO  
import time 
import pygame

  

#flag de sortie de boucle
accident_potentiel=0
state=0
    # set GPIO25 as input (button)  

#init lecteur audio
pygame.mixer.init()
pygame.mixer.music.set_volume(2.0)
		
#fonction play music
def play_music(state) :
	
	if state == 1:
		path = "/home/pi/Documents/Isenprotect/src/fichiers_audio/Alerte_collision_detectee.mp3"
	elif state == 2:
		path = "/home/pi/Documents/Isenprotect/src/fichiers_audio/Envoie_des_secours_a_votre_position.mp3"
	elif state == 3:
		path = "/home/pi/Documents/Isenprotect/src/fichiers_audio/Fin_d_alerte.mp3"

	pygame.mixer.music.load(path)
	pygame.mixer.music.play()

	while pygame.mixer.music.get_busy() == True:
   		continue
	





  
