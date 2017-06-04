#-*- coding: utf-8 -*-

import time
import random
import datetime
import logging
import telepot
import RPi.GPIO as GPIO
import time
from picamera import PiCamera

chat_id = -1

MyBotName = 'Jhoiti_Residencia'
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

def handle(msg):
    sensor = 7
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(sensor, GPIO.IN)	
    chat_id = msg['chat']['id']
    str_UserID = str(chat_id)
    command = msg['text'].lower()
    	
   
    print 'Comando Recebido: %s' % command

    logging.info("Usuario ID:{1} enviou comando {0}".format(command, str_UserID)) 

    def movimento(msg):
        bot.sendMessage(chat_id, text="Movimento Detectado")
        time.sleep(3)
        camera.start_preview()
        camera.capture('movimento.jpg')
   
        bot.sendPhoto(chat_id, photo=open('movimento.jpg', 'rb'))
        time.sleep(20)

    try:
        GPIO.add_event_detect(7, GPIO.RISING, movimento)
    except:
	GPIO.cleanup()


    try:
	    if command == '/start' or command == '/start@' + MyBotName.lower():
	        mensagem = "Ola usuario ID: {1}, eu sou o {0} do Telegram. ".format(MyBotName, str_UserID)
	        mensagem = mensagem + "Vc pode me controlar usando os seguintes " \
                                  "comandos:\n\n" \
                                  "/tirar_foto Tira a foto e envia \n" \
                                  "/time           Retorna a hora atual \n" \
                                  "/ligar_led   Liga o led vermelho \n " \

	        bot.sendMessage(chat_id, mensagem)

            elif command == '/tirar_foto':
                camera.start_preview()
                camera.capture('tirar_foto.jpg')
                bot.sendPhoto(chat_id, photo=open('tirar_foto.jpg', 'rb'))
                mensagem = 'Imagem capiturado com sucesso na data :'
                bot.sendMessage(chat_id, mensagem + str(datetime.datetime.now()))
                time.sleep(2)
                GPIO.cleanup(sensor, 7)

	    elif command == '/roll':
	         bot.sendMessage(chat_id, random.randint(1,6))

	    elif command == '/time':
	         bot.sendMessage(chat_id, str(datetime.datetime.now()))

	    elif command == '/ligar_led1':
                if not GPIO.input(18):
                  GPIO.output(18, 1)
                  mensagem = 'Led ligado'
                  bot.sendMessage(chat_id, mensagem)
                 #led_status = True

	    elif command == '/desligar_led1':
	         GPIO.output(18, 0)
	         mensagem = 'Led Desligado'
	         bot.sendMessage(chat_id, mensagem)
                #led_status = False
	         GPIO.cleanup(18)
	         
            elif command == '/ligar_led0':
                  GPIO.output(23, 1)
                  mensagem = 'Led ligado'
                  bot.sendMessage(chat_id, mensagem)
                 #led_status = True

	    elif command == '/desligar_led0':
	         GPIO.output(23, 0)
	         mensagem = 'Led Desligado'
	         bot.sendMessage(chat_id, mensagem)
                #led_status = False
	         GPIO.cleanup(23)

	    else:
	        mensagem = "Nao reconheco o comando {0}. Envie o comando /start para solicitar ajuda...".format(command)
	        bot.sendMessage(chat_id, mensagem)
    finally:
        pass


bot = telepot.Bot('342183200:AAEtDytfZquavOul-9Plci0hvyzJDhMlZiQ')
bot.message_loop(handle)
print 'Aguardando o comando ...'

while 1:
    time.sleep(10)
