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

#Based On Input File Name,
#Stores All iMessages Sent From User.
#Solely Dependent On Formatted CSV File.
def getAllSentMessages(inputFileName, startTimeStamp):
	#Open CSV File. 
	#currentFileReader = open(inputFileName, "r")
	allDesiredColumnValues = ['text', 'timestamp','is_sent', 'phone_number']
	allExtractData = pandas.read_csv(inputFileName, usecols=allDesiredColumnValues)
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
	print(len(allSentMessages))
	return allSentMessages

#Main Function For Running Sentiment Analysis,
#Based On Specifically Formatted CSV File 
#From iMessagesDataExtractor.py Extractor.
def runSentimentAnalysisAlgorithm(allSentMessages):
	return

#For Testing Purposes Only:
def main(inputFileName, prevLogDateTime):
	if(prevLogDateTime != None):
		prevLogDateTime = datetime.strptime(prevLogDateTime, '%Y-%m-%d %H:%M:%S')
	getAllSentMessages(inputFileName, prevLogDateTime)

if __name__ == '__main__':
	main("/Users/vsrinivas321/Documents/VSR_iMessages_Data.csv", "2020-06-20 12:53:20")