from PIL import Image
import os
import numpy as np

class imgconverter:

	def __init__(self):
		pass

	def write(self, image):
		img = Image.fromarray(np.array(image), 'L')
		img.save(os.getcwd() + '/data/test.png')

	def read(self, imagePath):
		image = Image.open(imagePath).convert('L')
		return np.asarray(image)