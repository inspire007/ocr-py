import os

DATA_DIR = os.getcwd() + '/data/'
TRAIN_DATA_CLASS_FILE = DATA_DIR + '/emnist_source_files/emnist-byclass-train-images-idx3-ubyte'
TRAIN_DATA_LABELS_FILE = DATA_DIR + '/emnist_source_files/emnist-byclass-train-labels-idx1-ubyte'


def get_training_data():
	pass

def read_training_file_bytes(filename, maximum = None):
	images = []
	if not os.path.exists(filename):
		raise Exception(f"File {filename} not found")

	with open(filename, 'rb') as file:
		file.seek(4)
		n_images = int.from_bytes(file.read(4))
		n_rows = int.from_bytes(file.read(4))
		n_cols = int.from_bytes(file.read(4))

		image = []
		for images_idx in range(n_images):
			for row_idx in range(n_rows):
				row = []
				for col_idx in range(n_cols):
					row.append(file.read(1))
				image.append(row)
			images.append(image)

			if(maximum and images_idx >= maximum):
				break

	return images


def main():
	train_data = read_training_file_bytes(TRAIN_DATA_CLASS_FILE, 5000)
	exit(0)

if __name__ == '__main__':
	main()