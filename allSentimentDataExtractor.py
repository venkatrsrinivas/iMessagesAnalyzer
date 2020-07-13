'''
Jai Sri Rama
Om Namah Shivaya
Har Har Mahadev
'''

#Import Python3 Libraries:
import sys
import csv
import pandas

#Based On Input File Name,
#Stores All iMessages Sent From User.
#Solely Dependent On Formatted CSV File.
def getAllSentMessages(inputFileName):
	#Open CSV File. 
	#currentFileReader = open(inputFileName, "r")
	allDesiredColumnValues = ['text', 'timestamp','is_sent', 'phone_number']
	allExtractData = pandas.read_csv(inputFileName, usecols=allDesiredColumnValues)
	allSentMessages = []
	#Loop Through Rows From CSV File.
	prevTimeStamp = None
	for currentData in allExtractData.iterrows():
		#Extract Data From Pandas Data-Frame:
		currentRowValue, (currentTextValue, currentTimeStamp, currentIsSent, currentPhoneNumber) = currentData
		#Comparing TimeStamps To Print Messages In Chronological Order Only:
		# if(prevTimeStamp == None or currentTimeStamp >= prevTimeStamp):
		# 	print(currentTimeStamp)
		# else:
		# 	prevTimeStamp = currentTimeStamp
		if(currentIsSent):
			formatSentMessages.append((currentTimeStamp, currentTextValue))
	return allSentMessages

#Main Function For Running Sentiment Analysis,
#Based On Specifically Formatted CSV File 
#From iMessagesDataExtractor.py Extractor.
def runSentimentAnalysisAlgorithm(allSentMessages):
	return

#For Testing Purposes Only:
def main():
	getAllSentMessages("/Users/vsrinivas321/Documents/VSR_iMessages_Data.csv")

if __name__ == '__main__':
	main()