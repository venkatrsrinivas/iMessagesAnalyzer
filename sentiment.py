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

#Home-Made Sentiment Analysis:
def runHomeMadeSentimentComputation():
	return

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
		allSentimentData.append((initialText, currentAnalyzer.polarity_scores(currentText)['compound']));

	#return computeAllNegativeMessages(allSentimentData)

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
		# 	#Simply Set Current Time Stamp = Prev Time Stamp,
		# 	#Which May Possibly Be None.
		# 	currentTimeStamp = prevTimeStamp;	
		# else:
		# 	currentTimeStamp = datetime.strptime(currentTimeStamp, '%Y-%m-%d %H:%M:%S')
		#Comparing TimeStamps To Store Only Messages >= startTimeStamp:
		# if(startTimeStamp == None 
		# 	or currentTimeStamp == None 
		# 	or currentTimeStamp >= startTimeStamp):

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
	# 	prevLogDateTime = datetime.strptime(prevLogDateTime, '%Y-%m-%d %H:%M:%S')
	#Compute All Sent Messages.
	allSentMessages, lastVisitedIndex = getAllSentMessages(inputFilePath, prevComputeIndex)
	#Run Sentiment Analysis ML/NLP Algorithms.
	#Return Appropriate Sentiment Data Back To Caller.
	#print(allSentMessages)
	return (runAllSentimentAnalysisAlgorithms(allSentMessages), lastVisitedIndex)

if __name__ == '__main__':
	main("/Users/vsrinivas321/Documents/VSR_iMessages_Data.csv", "2020-06-20 12:53:20")

