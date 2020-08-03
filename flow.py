'''
Jai Sri Rama
Om Namah Shivaya
Har Har Mahadev
'''

#TensorFlow Import Statements.
import tensorflow_datasets as tfds
import tensorflow as tf
from keras.models import model_from_json

def runTrainTestSave():
	# dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True,
	# 						  as_supervised=True)
	# encoder = info.features['text'].encoder
	# train_dataset, test_dataset = dataset['train'], dataset['test']
	# encoder = info.features['text'].encoder
	# BUFFER_SIZE = 10000
	# BATCH_SIZE = 64
	# train_dataset = train_dataset.shuffle(BUFFER_SIZE)
	# train_dataset = train_dataset.padded_batch(BATCH_SIZE)
	# test_dataset = test_dataset.padded_batch(BATCH_SIZE)
	# model = tf.keras.Sequential([
	# 	tf.keras.layers.Embedding(encoder.vocab_size, 64),
	# 	tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
	# 	tf.keras.layers.Dense(64, activation='relu'),
	# 	tf.keras.layers.Dense(1)    
	# ])
	# model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
	# 		  optimizer=tf.keras.optimizers.Adam(1e-4),
	# 		  metrics=['accuracy'])
	# history = model.fit(train_dataset, epochs=10,
	# 				validation_data=test_dataset, 
	# 				validation_steps=30)
	# test_loss, test_acc = model.evaluate(test_dataset)
	#Load JSON File w/ Model Data + Create Model:
	currentModelFile = open("allModelData.json", 'r')
	currentModelReader = currentModelFile.read()
	currentModelFile.close()
	model = model_from_json(currentModelReader)
	#Load Model w/ Weights:
	model.load_weights("allWeightData.h5")
	#Convert Trained Model To JSON File.
	currentJSON = model.to_json()
	#Write JSON File To Current Directory.
	with open("allModelData.json", "w") as currentFile:
	   currentFile.write(currentJSON)
	#Save/Serialize Weights To HDF5 File.
	model.save_weights("allWeightData.h5")

if __name__ == '__main__':
	runTrainTestSave()

