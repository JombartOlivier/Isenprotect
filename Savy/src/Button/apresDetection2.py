#!/usr/bin/env python2.7  

  
import RPi.GPIO as GPIO  
import time 

  

#flag de sortie de boucle
accident_potentiel=0

#setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) 							   #LED du bouton
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)    # set GPIO25 as input (button)  
  

# Define a threaded callback function to run in another thread when events are detected  
def my_callback(cha):  
	
    global accident_potentiel
    accident_potentiel=10
    print("interruption",accident_potentiel)

#detection changement d'état et appel de la fonction callback
GPIO.add_event_detect(25, GPIO.BOTH, callback=my_callback)

print ("entre dans la boucle")
#main
while accident_potentiel<10 :
	GPIO.output(18,GPIO.HIGH) #led clignote 
	print("Alerte, collision detectee, attente de confirmation")
	time.sleep(0.25) #pause 0.25s
	GPIO.output(18,GPIO.LOW)
	print(accident_potentiel)
	time.sleep(0.25)
	accident_potentiel+=1

print("sort de la boucle")	
	
			                






  
