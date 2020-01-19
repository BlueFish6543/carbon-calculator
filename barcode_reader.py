from pyzbar import pyzbar
from PIL import Image
import os

def get_barcode_from_image(image_data):
	return pyzbar.decode(image_data)

def scan(filename):

	# Image.open('pyzbar/tests/code128.png')

	img_data = Image.open(filename)
	barc = get_barcode_from_image(img_data)
	# print(barc)
	for b in barc:
		return b.data
	return
