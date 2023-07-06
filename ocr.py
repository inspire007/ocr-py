import os
import argparser
from PIL import Image

data_selector = 'mnist'
DATA_DIR = os.getcwd() + '/data/'
TRAIN_DATA_CLASS_FILE = DATA_DIR + f'/emnist_source_files/emnist-{data_selector}-train-images-idx3-ubyte'
TRAIN_DATA_LABELS_FILE = DATA_DIR + f'/emnist_source_files/emnist-{data_selector}-train-labels-idx1-ubyte'

TEST_DATA_CLASS_FILE = DATA_DIR + f'/emnist_source_files/emnist-{data_selector}-test-images-idx3-ubyte'
TEST_DATA_LABELS_FILE = DATA_DIR + f'/emnist_source_files/emnist-{data_selector}-test-labels-idx1-ubyte'


def int_from_bytes(data):
	return int.from_bytes(data, 'big')

def read_file_bytes(filename, maximum = None):
	images = []
	if not os.path.exists(filename):
		raise Exception(f"File {filename} not found")

	with open(filename, 'rb') as file:
		file.seek(4)
		n_images = int_from_bytes(file.read(4))
		n_rows = int_from_bytes(file.read(4))
		n_cols = int_from_bytes(file.read(4))

		#print(n_rows, n_cols, n_images)

		for images_idx in range(n_images):
			image = []
			for row_idx in range(n_rows):
				row = []
				for col_idx in range(n_cols):
					row.append(file.read(1))
				image.append(row)

			images.append(image)
			if(maximum and images_idx >= maximum):
				break

	return images

def read_labels(filename, maximum = None):

	labels = []
	if not os.path.exists(filename):
		raise Exception(f"File {filename} not found")

	with open(filename, 'rb') as file:
		file.seek(4)

		n_rows  = int_from_bytes(file.read(4))
		for label_idx in range(n_rows):
			labels.append((int_from_bytes(file.read(1))))
			if(maximum and label_idx >= maximum):
				break

	return labels


def convert_oned_pixel(image):
	return [pixel for X in image for pixel in X ]

def twod_oned(X):
	return [convert_oned_pixel(image) for image in X]

def calc_distance(X, Y):
	return sum(
		[
			( int_from_bytes(x_i) - int_from_bytes(y_i) )**2 for x_i, y_i in zip(X, Y)
		]
	) ** 0.5

def find_distances(test_one, train_data, k = 3):
	distances = [calc_distance(train_one, test_one) for train_one in train_data]
	distances = enumerate(distances)
	return find_shortest(distances, k)

def find_shortest(distances, k):
	sorted_list = sorted(distances, key=lambda x:x[1])
	return sorted_list[:k]

def find_trained_labels(sorted_distances, train_labels):
	labels = []
	for y in sorted_distances:
		label = [find_trained_label(x, train_labels) for (x, _) in list(y)]
		labels.append(label if len(label) > 1 else label[0])
	return labels

def find_trained_label(X, train_labels):
	return train_labels[X]

def main():
	train_data = twod_oned(read_file_bytes(TRAIN_DATA_CLASS_FILE, 1000))
	train_labels = read_labels(TRAIN_DATA_LABELS_FILE, 1000)

	test_data = twod_oned(read_file_bytes(TEST_DATA_CLASS_FILE, 2))
	test_labels = read_labels(TEST_DATA_LABELS_FILE, 2)

	distances = [find_distances(test_X, train_data, 1) for test_X in test_data]
	labels = find_trained_labels(distances, train_labels)

	print(f"Predictions: {labels}\n\nActual results: {test_labels}")



if __name__ == '__main__':
	parser = argparser.ArgumentParser()
	parser.add('--image', type=str, help="Specify image path")
	parser.add('--image', type=str, help="Specify image path")
	parser.add('--type', type=str, help="Specify type i.e. digits chars alphanumerical")
	args = parser.parse_arg()



	main()