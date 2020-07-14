'''
Jai Sri Rama
Om Namah Shivaya
Har Har Mahadev
'''

#Import Python3 Libraries:
import sys
import csv
import pandas
from datetime import datetime
from textblob import TextBlob
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
	print(allSentMessages)
	return allSentMessages

#Main Function For Running Sentiment Analysis,
#Based On Specifically Formatted CSV File 
#From iMessagesDataExtractor.py Extractor.
def runSentimentAnalysisAlgorithm(allSentMessages):
	#Setup For Tensor Flow + Machine Learning Algorithm.
	#In-Case No Messages Were Sent In Desired Time Frame.
	if(len(allSentMessages) == 0):
		return [];
	#Threshold For Negative-Text Message Classification = 0.5 Probability.
	#Return Pairing (CurrentText, Sentiment Classification).
	#Initialize Vader Sentiment Analyzer:
	currentAnalyzer = SentimentIntensityAnalyzer()
	for currentMessage in allSentMessages:
		#Replace In Case For Emojis:
		currentText = emoji.demojize(currentMessage[1]).replace(":", "").replace("_", " ")
		#Run Text Blob Sentiment Analyzer:
		currentSentiment = TextBlob(currentText).sentiment
		#Output All Sentiment Data.
		print(currentText, currentSentiment, currentAnalyzer.polarity_scores(currentText))

#For Testing Purposes Only:
def main(inputFilePath, prevLogDateTime):
	#Adjust Previous Log Date Time To Allow For Comparison Of Dates.
	if(prevLogDateTime != None or type(prevLogDateTime) != datetime):
		prevLogDateTime = datetime.strptime(prevLogDateTime, '%Y-%m-%d %H:%M:%S')
	#Compute All Sent Messages.
	allSentMessages = getAllSentMessages(inputFilePath, prevLogDateTime)
	#Run Sentiment Analysis ML/NLP Algorithms.
	runSentimentAnalysisAlgorithm(allSentMessages)
	#Return Appropriate Sentiment Data Back To Caller.
	return [];

if __name__ == '__main__':
	main("/Users/vsrinivas321/Documents/VSR_iMessages_Data.csv", "2020-06-20 12:53:20")