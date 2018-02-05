#!/usr/bin/env python3 
#coding : utf8
  
import RPi.GPIO as GPIO  
import time 
import pygame
  

#flag de sortie de boucle
accident_potentiel=0
valeur=0
#setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) 							   #LED du bouton
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (button)  

#init lecteur audio
pygame.mixer.init()
pygame.mixer.music.set_volume(2.0)



#fonction play music
def play_music() :

	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
   		continue

# Define a threaded callback function to run in another thread when events are detected  
def my_callback(cha):  
	
    global accident_potentiel
    global valeur
    accident_potentiel=10
    valeur=1
    


#detection changement d'état et appel de la fonction callback
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback)


#main
while accident_potentiel<10 :
	GPIO.output(18,GPIO.HIGH)   #led clignote 
	print("Alerte, collision detectee, attente de confirmation")
	pygame.mixer.music.load("Alerte_collision_detectee.wav")
	play_music()
	GPIO.output(18,GPIO.LOW)
	print(accident_potentiel)
	time.sleep(0.25)
	accident_potentiel+=1

if valeur==0:
	print("accident confirme, envoie des secours à votre position")
	pygame.mixer.music.load("Envoie_des_secours_ a_votre_position.wav")
	play_music()

else :	
	pygame.mixer.music.load("Fin_d_alerte.wav")
	play_music()





  
