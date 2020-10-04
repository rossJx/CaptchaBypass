#!/usr/bin/python3

import requests, time, os, signal, re, pytesseract
from PIL import Image
from pwn import *

#Variables globales
url = "http://127.0.0.1/captcha"

def def_handler(sig, frame):
	log.info("Saliendo del programa")
	os.remove("captcha.jpg")
	sys.exit(0)
	
signal.signal(signal.SIGINT, def_handler)

def makeRequest():
	
	status = 0
	
	while status == 0:
		try:
			s = requests.session()
			response = s.get(url)
			
			rand_value = re.search(r'\d{5,10}', response.text)
			url_image = url + "/captcha.php?rand=" + rand_value.group(0)
			
			captcha_url = s.get(url_image)
			
			f = open("captcha.jpg", "wb")
			f.write(captcha_url.content)
			f.close()
			
			p1 = log.progress("Captcha")
			p1.status("Obteniendo valor del Captcha")
			
			captcha_value = pytesseract.image_to_string(Image.open('captcha.jpg'))
			os.remove('captcha.jpg')
			
			p1.success("Captcha almacenado")
			
			print("\n--------------------> {}\n". format(captcha_value))
			
			post_data = {
				'captcha' : "{}".format(captcha_value),
				'submit' : 'Submit'
			}
			
			p2 = log.progress("Validacion")
			p2.status("Proporcionando Captcha")
			
			r2 = s.post(url, data = post_data)
			
			if "Entered captcha code does not match" not in r2.text and captcha_value.strip():
				p2.success("Captcha introducido correcto")
				status = 1
			else:
				p2.failure("Captcha introducido incorrecto")
				
		except Exception as e:
			log.failure("Ha ocurrido un error: {}".format(str(e)))
			sys.exit(1)
	
if __name__ == '__main__':
	makeRequest()
