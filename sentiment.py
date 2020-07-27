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


def TensorFlow():
	return

def convertAllEmojis(currentText):
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
	#Setup For Tensor Flow + Machine Learning Algorithm.
	#In-Case No Messages Were Sent In Desired Time Frame.
	if(len(allSentMessages) == 0):
		return [];
	#Threshold For Negative-Text Message Classification = 0.5 Probability.
	#Return Pairing (CurrentText, Sentiment Classification).
	#Combines Three Types of Sentiment Analyzer + Weights Them.
	#Initialize Vader Sentiment Analyzer:
	allSentMessages = [("", "Hello :)"), ("", "6:30-7:00"), ("", "Hello :)")];
	allSentimentData = [];
	currentAnalyzer = SentimentIntensityAnalyzer()
	for currentMessage in allSentMessages:
		#Make Copy Of Current Text To Match w/ Ouput Sentiment.
		initialText = currentMessage[1]
		#Replace Emoji w/ Relevant Text Fields.
		currentText = convertAllEmojis(initialText);
		print(initialText, currentText)
		#Run Text Blob Sentiment Analyzer:
		currentSentiment = TextBlob(currentText).sentiment
		#Debug Output For Understanding Sentiment:
		#print(currentText, currentSentiment, currentAnalyzer.polarity_scores(currentText))
		#print(initialText, currentAnalyzer.polarity_scores(currentText)['compound'])
		#Output All Sentiment Data.
		allSentimentData.append((initialText, currentAnalyzer.polarity_scores(currentText)['compound']));

	#return computeAllNegativeMessages(allSentimentData)

#Based On Input File Name,
#Stores All iMessages Sent From User.
#Solely Dependent On Formatted CSV File.
def getAllSentMessages(inputFilePath, startTimeStamp):
	#Open CSV File. 
	#currentFileReader = open(inputFileName, "r")
	allDesiredColumnValues = ['text', 'timestamp','is_sent', 'phone_number']
	allExtractData = pandas.read_csv(inputFilePath, usecols=allDesiredColumnValues)
	allSentMessages = []
	#Helper Variable To Maintain Prev Time Stamp While Looping.
	prevTimeStamp = None
	#Loop Through Rows From CSV File.
	for currentData in allExtractData.iterrows():
		#Extract Data From Pandas Data-Frame:
		currentRowValue, (currentTextValue, currentTimeStamp, currentIsSent, currentPhoneNumber) = currentData
		#Error-Check For Current Time Stamp As Empty + Not Proper String:
		if(not(isinstance(currentTimeStamp, str))):
			#Simply Set Current Time Stamp = Prev Time Stamp,
			#Which May Possibly Be None.s
			currentTimeStamp = prevTimeStamp;	
		else:
			currentTimeStamp = datetime.strptime(currentTimeStamp, '%Y-%m-%d %H:%M:%S')
		#Comparing TimeStamps To Store Only Messages >= startTimeStamp:
		if(startTimeStamp == None 
			or currentTimeStamp == None 
			or currentTimeStamp >= startTimeStamp):
			#Assert Message Is Sent.
			if(currentIsSent):
				allSentMessages.append((currentTimeStamp, currentTextValue))
		prevTimeStamp = currentTimeStamp;
	#Return All Sent Messages.
	#print(allSentMessages)
	return allSentMessages

#For Testing Purposes Only:
def main(inputFilePath, prevLogDateTime):
	#Adjust Previous Log Date Time To Allow For Comparison Of Dates.
	if(prevLogDateTime != None or type(prevLogDateTime) != datetime):
		prevLogDateTime = datetime.strptime(prevLogDateTime, '%Y-%m-%d %H:%M:%S')
	#Compute All Sent Messages.
	allSentMessages = getAllSentMessages(inputFilePath, prevLogDateTime)
	#Run Sentiment Analysis ML/NLP Algorithms.
	runAllSentimentAnalysisAlgorithms(allSentMessages)
	#Return Appropriate Sentiment Data Back To Caller.
	return [];

if __name__ == '__main__':
	main("/Users/vsrinivas321/Documents/VSR_iMessages_Data.csv", "2020-06-20 12:53:20")

