'''
Jai Sri Rama
Om Namah Shivaya
Har Har Mahadev
'''

#TensorFlow Import Statements.
import tensorflow as tf
import tensorflow_datasets as tfds
from keras.models import model_from_json

#Main Driver Training + Testing Function.
def runTrainTestSave():
	#Load All Movie Review Data Set + Related Information:
	currentDataSet, currentInfoData = tfds.load('imdb_reviews/subwords8k', with_info=True,
							  as_supervised=True)
	#Split Data Into Train + Test Frameworks:
	trainDataSet, testDataSet = currentDataSet['train'], currentDataSet['test']
	currentEncoder = currentInfoData.features['text'].encoder
	#Initialize Key Training + Testing Sample Sizes:
	BUFFER_SIZE = 10000
	BATCH_SIZE = 64
	#Shuffle Train + Test Data:
	trainDataSet = trainDataSet.shuffle(BUFFER_SIZE)
	trainDataSet = trainDataSet.padded_batch(BATCH_SIZE)
	testDataSet = testDataSet.padded_batch(BATCH_SIZE)
	#Initialize Current Model:
	currentModel = tf.keras.Sequential([
		tf.keras.layers.Embedding(currentEncoder.vocab_size, 64),
		tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
		tf.keras.layers.Dense(64, activation='relu'),
		tf.keras.layers.Dense(1)    
	])
	#Compilation of Model:
	currentModel.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
			  optimizer=tf.keras.optimizers.Adam(1e-4),
			  metrics=['accuracy'])
	#Fit Current Model Based On Trainin Data.
	#Make Model Learn Training Data + Validate On Testing Data.
	allHistoryData = currentModel.fit(trainDataSet, epochs=10,
					validation_data=testDataSet, 
					validation_steps=30)
	#Evaluate Final Performance On Testing Data.
	testLoss, testAccuracy = currentModel.evaluate(testDataSet)
	#Output To Terminal Console:
	print("Test Loss: " + str(testLoss) + " + Test Accuracy: " + str(testAccuracy))
	#Load JSON File w/ Model Data + Create Model:
	currentModelFile = open("allModelData.json", 'r')
	currentModelReader = currentModelFile.read()
	currentModelFile.close()
	currentModel = model_from_json(currentModelReader)
	#Load Model w/ Weights:
	currentModel.load_weights("allWeightData.h5")
	#Convert Trained Model To JSON File.
	currentJSON = currentModel.to_json()
	#Write JSON File To Current Directory.
	with open("allModelData.json", "w") as currentFile:
	   currentFile.write(currentJSON)
	#Save/Serialize Weights To HDF5 File.
	currentModel.save_weights("allWeightData.h5")

#Main Driver Caller/Invoker:
if __name__ == '__main__':
	runTrainTestSave()

