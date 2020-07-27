'''
Jai Sri Rama
Om Namah Shivaya
Har Har Mahadev
'''

#Import All Relevant Python3 Libraries.
import sqlite3
import pandas
from datetime import datetime

#Heler Function Devised To Populate iMessages Data From inputPathToRead,
#To An Output CSV File, Specified By inputPathToWrite.
def populateMessagesDataToCSV(inputPathToRead, inputPathToWrite):
	#The Below Python3 Script Is Used To Obtain 
	#All Message History Present From Input Mac. 
	#The Below Code Was Adopted From Yorgos Askalidis,
	#w/ GitHub Username: yortos.
	#Therefore, All Credits Go To Their Team.

	#Here Is The Link To Their GitHub Repository 
	#Containing  The Tutorial As Well As 
	#More Information On iMessages Data Extraction:
	#https://github.com/yortos/imessage-analysis

	#Find The chat.db Database File Holding All Message Data 
	#+ Establish SQLite3 Connection.
	#Note: Replace vsrinivas321 w/ Appropriate Apple ID Mac Username.
	try:
		currentConnection = sqlite3.connect(inputPathToRead)
	except:
		print("Fatal Error: Could Not Connect To Chat Database File From The Following Path: ", inputPathToRead)
		#Inform Client w/ Failure Status.
		return -1;

	#Initialize Current Reader To Extract Data.
	currentReader = currentConnection.cursor()

	#Try Querying Database To Get All Table Names.
	try:
		currentReader.execute(" select name from sqlite_master where type = 'table' ")	
	except:
		print("Fatal Error: Could Not Find Desired Table Data.")
		return -1;

	#Print All Table Data Prior To Reading SQL Data.
	#Uncomment To View Data Parameters + All Relevant Information Encapsulated.
	#for currentField in currentReader.fetchall():
	    #print(currentField)

	#Create Pandas Dataframe w/ All Relevant Database Tables.
	allMessagesData = pandas.read_sql_query('''select *, datetime(date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime")  as date_utc from message''', currentConnection) 
	allHandlesData = pandas.read_sql_query("select * from handle", currentConnection)
	allChatMessageJoinData = pandas.read_sql_query("select * from chat_message_join", currentConnection)

	#Code Used Related To Fields, Useful For Only DateTime Analysis 
	#(e.g., # Messages/Month, # Messages/Year, ...)
	allMessagesData['message_date'] = allMessagesData['date']
	allMessagesData['timestamp'] = allMessagesData['date_utc'].apply(lambda x: pandas.Timestamp(x))
	allMessagesData['date'] = allMessagesData['timestamp'].apply(lambda x: x.date())
	allMessagesData['month'] = allMessagesData['timestamp'].apply(lambda x: int(x.month))
	allMessagesData['year'] = allMessagesData['timestamp'].apply(lambda x: int(x.year))

	#Rename ROWID into message_id = # Numerical Value For Particular Message.
	allMessagesData.rename(columns={'ROWID' : 'message_id'}, inplace = True)
	#Rename Handle and Phone Number.
	allHandlesData.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)

	#Merge allMessagesData + allHandlesData.
	allMergeData = pandas.merge(allMessagesData[['text', 'handle_id', 'date','message_date' ,'timestamp', 'month','year','is_sent', 'message_id']],  allHandlesData[['handle_id', 'phone_number']], on ='handle_id', how='left')
	#Now Merge Messages w/ Chats.
	finalMessagesData = pandas.merge(allMergeData, allChatMessageJoinData[['chat_id', 'message_id']], on = 'message_id', how='left')

	#Random Debugging. 
	#Can Write Code To Extract Messages To/From A Particular Phone Number.
	#print(finalMessagesData['phone_number'])

	#Note: Replace vsrinivas321 w/ Apple ID Mac Username.
	#Output To CSV For File Viewing.
	print("START: Finished Extracting + Formatting iMessages Data + Outputting To CSV.")
	finalMessagesData.to_csv(inputPathToWrite, index = False, encoding='utf-8')
	print("END: Finished Output To CSV. All iMessages Data Ready For Viewing.")
	return 0;

#Main Driver Functions:
if __name__ == '__main__':
	populateMessagesDataToCSV(sys.argv[0], sys.argv[1]);

