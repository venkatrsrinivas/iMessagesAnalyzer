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
	
	print("Welcome To iMessagesSentimentAnalyzer, Your Own iMessages Data Sentiment Analysis Client.\n");
	existUserEmail = input("Enter Your User-Email, Even If You Are Not Registered: ");
	#Filter User Objects By Distinct Email.
	allExistObjects = User.objects.filter(currentEmail=existUserEmail);
	existUserObject = None
	#Special Case: User Is Currently Un-Registered.
	if(len(allExistObjects) == 0):
		print("\nHello! It Seems That You Are Currently Not Registered.");
		#Grab User Input For Other Key Parameters.
		newUserName = input("Enter Your Preferred User-Name: ");
		newUserEmail = existUserEmail;
		newUserIndex = 1;
		print("\nNow, We Must Identify The Path To Your chat.db Chat Database File.");
		print("For Example, This May Look Something Like The Following: /Users/vsrinivas321/Library/Messages/chat.db\n");
		newUserReadPath = input("Enter Your Current Chat Database Path: ")
		print("\nFinally, Enter The Desired Path To Store All Of Your Apple iMessages CSV Data.")
		print("For Example, This May Look Something Like The Following: /Users/vsrinivas321/Documents/VSR_iMessages_Data.csv\n");
		newUserWritePath = input("Enter Your Current Desired Path To Output Extracted Data: ")
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
	print();
	isSuccessExtract = extract.populateMessagesDataToCSV(existUserObject.currentPathToRead, existUserObject.currentPathToWrite)
	if(isSuccessExtract < 0):
		print("Fatal Error: Could Not Extract Desired Data.")
		return;
	allNegativeData, lastVisitedIndex = sentiment.main(existUserObject.currentPathToWrite, existUserObject.prevComputeIndex)
	for currentNegativeData in allNegativeData:
		print(currentNegativeData)
	existUserObject.prevComputeIndex = lastVisitedIndex;
	existUserObject.save();

#Main Driver Functions:	
if __name__ == '__main__':
	main()