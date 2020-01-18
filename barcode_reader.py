from pyzbar import pyzbar
from PIL import Image
import os

def get_barcode_from_image(image_data):
	return pyzbar.decode(image_data)

def main():
	print("kek")

	# Image.open('pyzbar/tests/code128.png')

	for file in os.listdir("carbon-calculator/barcodes"):
		img_data = Image.open(os.path.join("carbon-calculator/barcodes", file))
		print(file)
		barc = get_barcode_from_image(img_data)
		# print(barc)
		for b in barc:
			print(b.data)



if __name__ == '__main__':
	main()