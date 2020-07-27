'''
Jai Sri Rama
Om Namah Shivaya
Har Har Mahadev
'''

import sys
import os
import django
import extract
import sentiment

#Necessary Setup To Import Models:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iMessagesAnalyzer.settings")
django.setup()

from register.models import User

def main():
	#Grab Current User Based On System Arguments.
	#If Input Matches User, Continue.
	#Otherwise, Create New User + Continue.
	#If Subscribed, Then Continue.
	#Otherwise, Return To Terminate.

	#Current Basic Implementation: Assume User Is Subscribed.
	#Prompt User To Understand Whether They Have An Account.
	
	print("Welcome To iMessagesSentimentAnalyzer, Your Own iMessages Data Sentiment Analysis Client.");
	existUserEmail = input("Enter Your Registered Email. If Not Registered, Still Enter Your Desired Email For Communication.\n");
	#Filter User Objects By Distinct Email.
	allExistObjects = User.objects.filter(currentEmail=existUserEmail);
	existUserObject = None
	#Special Case: User Is Currently Un-Registered.
	if(len(allExistObjects) == 0):
		print("Hello! It Seems That You Are Currently Not Registered.");
		#Grab User Input For Other Key Parameters.
		newUserName = input("Enter Your Name:\n");
		newUserEmail = existUserEmail;
		newUserIndex = 1;
		print("Now, We Must Identify The Path To Your chat.db Chat Database File.");
		print("For Example, This May Look Something Like The Following: /Users/vsrinivas321/Library/Messages/chat.db");
		newUserReadPath = input("Search Your Apple Device For The Path To Your chat.db File + Correctly Input It Below.\n")
		print("Finally, Enter The Desired Path To Write All Of Your Apple iMessages CSV Data. This Is The Path To The File Where All Of The Key Data Will Be Stored.")
		print("For Example, This May Look Something Like The Following: /Users/vsrinivas321/Documents/VSR_iMessages_Data.csv");
		newUserWritePath = input("Search Your Apple Device For The Desired Path To Output Extracted Data.\n")
		existUserObject = User(currentEmail=newUserEmail,
								currentName=newUserName, 					
								currentPathToRead=newUserReadPath,
								currentPathToWrite=newUserWritePath,
								prevComputeIndex=newUserIndex);
		existUserObject.save();
	#Normal Case: User Is Already Registered.
	else:
		existUserObject = allExistObjects[0]

	#At This Point, The Existing User Object Should Have
	#Been Appropriately Created Or Simply Found.
	isSuccessExtract = extract.populateMessagesDataToCSV(existUserObject.currentPathToRead, existUserObject.currentPathToWrite)
	if(isSuccessExtract < 0):
		print("Fatal Error: Could Not Extract Desired Data.")
		return;
	allSentimentData, lastVisitedIndex = sentiment.main(existUserObject.currentPathToWrite, existUserObject.prevComputeIndex)
	existUserObject.prevComputeIndex = lastVisitedIndex;
	existUserObject.save();

#Main Driver Functions:	
if __name__ == '__main__':
	main()