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

#Global Variables For TensorFlow computations:
dataset, info = tfds.load('imdb_reviews/subwords8k', with_info=True,
							  as_supervised=True)
encoder = info.features['text'].encoder
#Load JSON File w/ Model Data + Create Model:
currentModelFile = open("allModelData.json", 'r')
currentModelReader = currentModelFile.read()
currentModelFile.close()
model = model_from_json(currentModelReader)
#Load Model w/ Weights:
model.load_weights("allWeightData.h5")

def pad_to_size(vec, size):
	zeros = [0] * (size - len(vec))
	vec.extend(zeros)
	return vec

def sample_predict(sample_pred_text, pad):
	encoded_sample_pred_text = encoder.encode(sample_pred_text)
	if pad:
		encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
	encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
	predictions = model.predict(tf.expand_dims(encoded_sample_pred_text, 0))

	return predictions

#"Home-Made" TensorFlow Sentiment Analysis:
def runHomeMadeSentimentComputation(currentText):
	sample_pred_text = currentText
	predictions = sample_predict(sample_pred_text, pad=False)
	return predictions

#Compute All Negatively Connotated Messages:
def computeAllNegativeMessages(allSentimentData):
	#Sort Tuples In All Sentiment Data Based On First Value.
	allSentimentData.sort(key = lambda currentPair: currentPair[0])
	#Return First 10 Unique Elements.
	allTenNegativeData = [];
	k = 0; 
	while(k < len(allSentimentData) and len(allTenNegativeData) < 10):
		currentText = allSentimentData[k][1].replace("\n", " ");
		if(not(currentText in allTenNegativeData)):
			allTenNegativeData.append(currentText);
		k += 1;
	return allTenNegativeData

#Compute All Positively Connotated Messages:
def computeAllPositiveMessages(allSentimentData):
	#Sort Tuples In All Sentiment Data Based On First Value.
	allSentimentData.sort(key = lambda currentPair: currentPair[0])
	#Return First 10 Elements.
	allTenNegativeData = [];
	for k in range(1, 11):
		if(k >= len(allSentimentData)):
			break;
		allTenNegativeData.append(allSentimentData[-k][1].replace("\n", " "))
	return allTenNegativeData

#Helper Function To Properly Handle Special Cases 
#w/ Emo = Emojis + Emoticons.
def convertAllEmo(currentText):
	#Convert All Real Emojis To Readable Text.
	for currentEmoji in UNICODE_EMO:
		currentText = currentText.replace(currentEmoji, " ".join(UNICODE_EMO[currentEmoji].replace("_", " ").replace(",","").replace(":","").split()))
	#Convert All String Representations Of Emojis To Readable Text.
	for currentEmoji in EMOTICONS:
		#print(currentEmoji, EMOTICONS[currentEmoji])
		allTextData = currentText.split();
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
		return [];
	#Threshold For Negative-Text Message Classification = 0.5 Probability.
	#Return Pairing (CurrentText, Sentiment Classification).
	#Combines Three Types of Sentiment Analyzer + Weights Them.
	#Initialize Vader Sentiment Analyzer:
	allSentimentData = [];
	currentAnalyzer = SentimentIntensityAnalyzer()
	for currentMessage in allSentMessages:
		#Make Copy Of Current Text To Match w/ Ouput Sentiment.
		initialText = currentMessage[1]
		#Replace Emoji + Emoticons w/ Relevant Text Fields.
		currentText = convertAllEmo(initialText);
		#print(initialText, currentText)
		#Run Text Blob Sentiment Analyzer:
		currentSentiment = TextBlob(currentText).sentiment
		#Debug Output For Understanding Sentiment:
		#print(currentText, currentSentiment, currentAnalyzer.polarity_scores(currentText))
		#print(initialText, currentAnalyzer.polarity_scores(currentText)['compound'])
		#Output All Sentiment Data.
		combineSentimentValue = currentAnalyzer.polarity_scores(currentText)['compound']
		tValue = runHomeMadeSentimentComputation(currentText)
		print(currentText, tValue)
		allSentimentData.append((combineSentimentValue, initialText));

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
	currentIndex = 0;

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
		#   currentTimeStamp = prevTimeStamp;   
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
		#prevTimeStamp = currentTimeStamp;
		#Increment Counter For Current Row Visited.
		currentIndex += 1;
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

if __name__ == '__main__':
	main("/Users/vsrinivas321/Documents/VSR_iMessages_Data.csv", 1)

