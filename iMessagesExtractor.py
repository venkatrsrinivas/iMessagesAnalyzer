#Python3 Script To Obtain All Message History Present On Mac. 
#The Below Code Was Adopted From Yorgos Askalidis (GitHub: yortos).
#Therefore, All Credits Go To Him.

#Here Is The Link To His GitHub Repository For The Tutortial 
#	+ Containing More Information On iMessage Data Extraction:
#		https://github.com/yortos/imessage-analysis

#Python3 Library Import.
import sqlite3
import pandas
from datetime import datetime

#---------------------------------------------------------------------#

#Find The chat.db Database File Holding All Message Data + Establish SQLite3 Connection.
#Note: Replace vsrinivas321 w/ Apple ID Mac Username.
currentConnection = sqlite3.connect('/Users/vsrinivas321/Library/Messages/chat.db')
currentReader = currentConnection.cursor()

#Query Database To Get All Table Names
currentReader.execute(" select name from sqlite_master where type = 'table' ")

#Print All Table Data Prior To Reading SQL Data.
#Uncomment To View Data Parameters + All Relevant Information Encapsulated.
#for currentField in currentReader.fetchall():
    #print(currentField)

#---------------------------------------------------------------------#

#Create Pandas Dataframe w/ All Relevant Database Tables.
allMessagesData = pandas.read_sql_query('''select *, datetime(date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime")  as date_utc from message''', currentConnection) 
allHandlesData = pandas.read_sql_query("select * from handle", currentConnection)
allChatMessageJoinData = pandas.read_sql_query("select * from chat_message_join", currentConnection)

#------------------------------------------------------------------------------#

#Code Used Related To Fields, Useful For Only DateTime Analysis 
#	(e.g., # Messages/Month, #Messages/Year, ...)
allMessagesData['message_date'] = allMessagesData['date']
allMessagesData['timestamp'] = allMessagesData['date_utc'].apply(lambda x: pandas.Timestamp(x))
allMessagesData['date'] = allMessagesData['timestamp'].apply(lambda x: x.date())
allMessagesData['month'] = allMessagesData['timestamp'].apply(lambda x: int(x.month))
allMessagesData['year'] = allMessagesData['timestamp'].apply(lambda x: int(x.year))

#Rename ROWID into message_id = # Numerical Value For Particular Message
allMessagesData.rename(columns={'ROWID' : 'message_id'}, inplace = True)
#Rename Handle and Phone Number.
allHandlesData.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)

#------------------------------------------------------------------------------------#

#Merge allMessagesData + allHandlesData.
allMergeData = pandas.merge(allMessagesData[['text', 'handle_id', 'date','message_date' ,'timestamp', 'month','year','is_sent', 'message_id']],  allHandlesData[['handle_id', 'phone_number']], on ='handle_id', how='left')
#Now Merge Messages w/ Chats.
finalMessagesData = pandas.merge(allMergeData, allChatMessageJoinData[['chat_id', 'message_id']], on = 'message_id', how='left')

#---------------------------------------------------------------------#

#Output To CSV For File Viewing.

#Random Debugging. 
#Can Write Code To Extract Messages To/From A Particular Phone Number.
#print(finalMessagesData['phone_number'])

#Note: Replace vsrinivas321 w/ Apple ID Mac Username.
print("START: Finished Extracting + Formatting iMessages Data + Outputting To CSV.")
finalMessagesData.to_csv('/Users/vsrinivas321/Documents/VSR_iMessages_Data.csv', index = False, encoding='utf-8')
print("END: Finished Output To CSV. All iMessages Data Ready For Viewing.")
