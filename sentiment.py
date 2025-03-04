'''
Jai Sri Rama
Om Namah Shivaya
Har Har Mahadev
'''
 
#Import Python3 Libraries:
import sys
import csv
import pandas
import emoji
import re
from emot.emo_unicode import UNICODE_EMO, EMOTICONS
from datetime import datetime
#Key Sentiment Analysis Import Statements.
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#TensorFlow Import Statements.
import tensorflow_datasets as tfds
import tensorflow as tf
from keras.models import model_from_json
import string

#Global Variables For TensorFlow Computations:
#Must Fix, Text Encoders Depreciating Eventually ...
#Link For Alternative Datasets: 
#	https://www.tensorflow.org/datasets/catalog/imdb_reviews
currentDataSet, currentInfoData = tfds.load('imdb_reviews/subwords8k', with_info=True,
							  as_supervised=True)
currentEncoder = currentInfoData.features['text'].encoder
#Load JSON File w/ Model Data + HDF5 File w/ Weight Data:
currentModelFile = open("allModelData.json", 'r')
currentModelReader = currentModelFile.read()
currentModelFile.close()
#Convert JSON File Reader To Model Object.
currentModel = model_from_json(currentModelReader)
#Load Model w/ Pre-Computed Weights:
currentModel.load_weights("allWeightData.h5")

#Key Links Dealing w/ Object Replacement Character Output Bug:
#	1. https://en.wikipedia.org/wiki/Specials_(Unicode_block)
#	2. https://www.compart.com/en/unicode/U+FFFC
#	3. https://www.fileformat.info/info/unicode/char/fffc/index.htm

#Helper Function To Pad Zeros To Current Vector.
def runPadZeros(currentVector, desireSize):
	allZeroData = [0] * (desireSize - len(currentVector))
	currentVector.extend(allZeroData)
	return currentVector

#Helper Function To Predict Based On Model:
def computeSamplePrediction(inputPredictText, isPadOn):
	#Encode Input Sample Predict Text To Run Through Model.
	currentEncodePredictText = currentEncoder.encode(inputPredictText)
	#Pad Additional Zeros, As Necessary.
	if(isPadOn):
		currentEncodePredictText = runPadZeros(currentEncodePredictText, 64)
	#Appropriately Cast Predict Text.
	currentEncodePredictText = tf.cast(currentEncodePredictText, tf.float32)
	allPredictionData = currentModel.predict(tf.expand_dims(currentEncodePredictText, 0))
	return allPredictionData

#"Home-Made" TensorFlow Sentiment Analysis:
def runHomeMadeSentimentComputation(inputPredictText):
	allPredictionData = computeSamplePrediction(inputPredictText, isPadOn=False)
	return allPredictionData[0][0]

#Compute All Negatively Connotated Messages:
def computeAllNegativeMessages(allSentimentData):
	#Sort Tuples In All Sentiment Data Based On First Value.
	allSentimentData.sort(key = lambda currentPair: currentPair[0])
	#Return First 10 Unique Elements.
	allTenNegativeData = []
	#Loop Through All Sorted Sentiment Data Or Until Ten Negative Messages Found.
	k = 0 
	while(k < len(allSentimentData) and len(allTenNegativeData) < 10):
		allTenNegativeData.append(allSentimentData[k][1])
		k += 1
	return allTenNegativeData

#Compute All Positively Connotated Messages:
def computeAllPositiveMessages(allSentimentData):
	#Sort Tuples In All Sentiment Data Based On First Value.
	allSentimentData.sort(key = lambda currentPair: currentPair[0])
	#Return First 10 Elements.
	allTenPositiveData = []
	#Loop Through All Sorted Sentiment Data Or Until Ten Positive Messages Found.
	#NOTE: Start At k = 1 Since We Are Using -k Operator.
	k = 1 
	while(k <= len(allSentimentData) and len(allTenPositiveData) < 10):
		allTenPositiveData.append(allSentimentData[-k][1])
		k += 1
	return allTenPositiveData

#Helper Function To Properly Handle Special Cases 
#w/ Emo = Emojis + Emoticons.
def convertAllEmo(currentText):
	#Convert All Real Emojis To Readable Text.
	for currentEmoji in UNICODE_EMO:
		currentText = currentText.replace(currentEmoji, " ".join(UNICODE_EMO[currentEmoji].replace("_", " ").replace(",","").replace(":","").split()))
	#Convert All String Representations Of Emojis To Readable Text.
	for currentEmoji in EMOTICONS:
		#print(currentEmoji, EMOTICONS[currentEmoji])
		allTextData = currentText.split()
		#currentText = re.sub(r'\b'+currentEmoji+'\b', " ".join(EMOTICONS[currentEmoji].replace(",","").split()), currentText)
		currentText = re.sub(u'( '+currentEmoji+')', " " + " ".join(EMOTICONS[currentEmoji].replace(",","").split()), currentText)
	return currentText

#Main Function For Running Sentiment Analysis,
#Based On Specifically Formatted CSV File 
#From iMessagesDataExtractor.py Extractor.
def runAllSentimentAnalysisAlgorithms(allSentMessages):
	print("Start: About To Run All Sentiment Analysis Algorithms.")
	#Setup For Tensor Flow + Machine Learning Algorithm.
	#In-Case No Messages Were Sent In Desired Time Frame.
	if(len(allSentMessages) == 0):
		return ([], [])
	#Threshold For Negative-Text Message Classification = 0.5 Probability.
	#Return Pairing (CurrentText, Sentiment Classification).
	#Combines Three Types of Sentiment Analyzer + Weights Them.
	#Initialize Vader Sentiment Analyzer:
	allSentimentData = []
	currentAnalyzer = SentimentIntensityAnalyzer()
	for currentMessage in allSentMessages:
		#Make Copy Of Current Text To Match w/ Ouput Sentiment.
		initialText = currentMessage[1]
		#Replace Emoji + Emoticons w/ Relevant Text Fields.
		convertText = convertAllEmo(initialText)
		#print(initialText, convertText)
		#Run Text Blob Sentiment Analyzer:
		bValue = TextBlob(convertText).sentiment.polarity
		#Debug Output For Understanding Sentiment:
		#print(convertText, currentSentiment, currentAnalyzer.polarity_scores(convertText))
		#print(initialText, currentAnalyzer.polarity_scores(convertText)['compound'])
		#Output All Sentiment Data.
		vValue = currentAnalyzer.polarity_scores(convertText)['compound']
		tValue = runHomeMadeSentimentComputation(convertText)
		combineSentimentValue = (bValue+vValue+tValue)/3
		#Check If Current Text Message Is Unique, Un-Visited, Significant.
		formatInitialText = initialText.replace("\n", " ").replace("\uFFFC", "")
		if(len(formatInitialText) > 0 
			and not(formatInitialText == "" or formatInitialText.isspace())
			and not(formatInitialText in allSentimentData)):	
			allSentimentData.append((combineSentimentValue, formatInitialText))

	print("End: Computed All Combined Sentiment Values.")
	allNegativeData = computeAllNegativeMessages(allSentimentData)
	allPositiveData = computeAllPositiveMessages(allSentimentData)
	#Let Client Format Data Appropriately As Desired.
	return (allPositiveData, allNegativeData)

#Based On Input File Name,
#Stores All iMessages Sent From User.
#Solely Dependent On Formatted CSV File.
def getAllSentMessages(inputFilePath, prevComputeIndex):
	#Open CSV File. 
	#currentFileReader = open(inputFileName, "r")
	allDesiredColumnValues = ['text', 'timestamp','is_sent', 'phone_number']
	allExtractData = pandas.read_csv(inputFilePath, usecols=allDesiredColumnValues)
	allSentMessages = []
	currentIndex = 0

	#Helper Variable To Maintain Prev Time Stamp While Looping.
	#prevTimeStamp = None
	#Loop Through Rows From CSV File.

	for currentData in allExtractData.iterrows():
		#Extract Data From Pandas Data-Frame:
		currentRowValue, (currentTextValue, currentTimeStamp, currentIsSent, currentPhoneNumber) = currentData
		
		#Old Date-Time Related Code.
		#Error-Check For Current Time Stamp As Empty + Not Proper String:
		# if(not(isinstance(currentTimeStamp, str))):
		#   #Simply Set Current Time Stamp = Prev Time Stamp,
		#   #Which May Possibly Be None.
		#   currentTimeStamp = prevTimeStamp   
		# else:
		#   currentTimeStamp = datetime.strptime(currentTimeStamp, '%Y-%m-%d %H:%M:%S')
		#Comparing TimeStamps To Store Only Messages >= startTimeStamp:
		# if(startTimeStamp == None 
		#   or currentTimeStamp == None 
		#   or currentTimeStamp >= startTimeStamp):

		#Skip Over Rows Already Visited.
		if(currentIndex >= prevComputeIndex):
			#Assert Message Is Sent From Current Device Owner.
			if(currentIsSent):
				allSentMessages.append((currentTimeStamp, currentTextValue))
		#prevTimeStamp = currentTimeStamp
		#Increment Counter For Current Row Visited.
		currentIndex += 1
	#Return All Sent Messages.
	#print(allSentMessages)
	return (allSentMessages, currentIndex)

#For Testing Purposes Only:
def main(inputFilePath, prevComputeIndex):
	#NOTE: Initially I Had It So That Data Was Computed After A Particular Date-Time.
	#But To Be Safe + Accurate, Simply Store # Last Visited Row.
	#Comparing TimeStamps To Store Only Messages >= startTimeStamp:
	#Adjust Previous Log Date Time To Allow For Comparison Of Dates.
	# if(prevLogDateTime != None or type(prevLogDateTime) != datetime):
	#   prevLogDateTime = datetime.strptime(prevLogDateTime, '%Y-%m-%d %H:%M:%S')
	#Compute All Sent Messages.
	allSentMessages, lastVisitedIndex = getAllSentMessages(inputFilePath, prevComputeIndex)
	#Run Sentiment Analysis ML/NLP Algorithms.
	#Return Appropriate Sentiment Data Back To Caller.
	#print(allSentMessages)
	return (runAllSentimentAnalysisAlgorithms(allSentMessages), lastVisitedIndex)

#Main Driver Invoker:
if __name__ == '__main__':
	inputFilePath = "/Users/vsrinivas321/Documents/VSR_iMessages_Data.csv"
	#Ask User If They Want To Specify Path:
	isPathWant = input("Enter 1 = Specify Input File Path, 0 = Use Existing Path From Script.\n")
	if(str(isPathWant) == "1"):
		inputFilePath = input("Enter Correct File Path Housing All iMesssages Data.\n")
	main(inputFilePath, 1)
