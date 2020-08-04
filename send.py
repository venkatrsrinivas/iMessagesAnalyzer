'''
Jai Sri Rama
Om Namah Shivaya
Har Har Mahadev
'''

#Relevant Python3 Import Libraries.
import sys
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

#Adopted/Learned From: 
#https://stackoverflow.com/questions/778202/smtplib-and-gmail-python-script-problems.

#Helper Function To Create Email Message Object w/ Padded Information.
def createMessageObject(inputFromAddress, inputToAddress, 
	inputSubjectData, inputBodyData):
	currentMessageObject = MIMEText(inputBodyData)
	currentMessageObject['Subject'] = inputSubjectData
	currentMessageObject['From'] = inputFromAddress
	currentMessageObject['To'] = inputToAddress
	currentMessageObject['Date'] = formatdate()
	return currentMessageObject

#Helper Function To Open SMTP Server + Send Email Data.
def runSendMail(inputFromAddress, inputToAddress, 
	inputPasswordData, currentMessageObject):
	smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpobj.ehlo()
	smtpobj.starttls()
	smtpobj.ehlo()
	smtpobj.login(inputFromAddress, inputPasswordData)
	smtpobj.sendmail(inputFromAddress, inputToAddress, currentMessageObject.as_string())
	smtpobj.close()

#Simple Script That Sends An Email 
#Given Input Email Address + Input Text Blocks.
def sendTimedEmails(inputEmailAddress, inputSubjectData, inputBodyData):
	currentFromAddress = 'vsrdev23@gmail.com'
	currentPasswordData = '23@JustTestAccount'
	currentToAddress = inputEmailAddress
	currentSubjectData = inputSubjectData
	currentBodyData = inputBodyData
	currentMessageObject = createMessageObject(currentFromAddress, currentToAddress, 
		currentSubjectData, currentBodyData)
	runSendMail(currentFromAddress, currentToAddress, currentPasswordData, currentMessageObject)

#Automatically Invoked Main Driver Function:
if __name__ == '__main__':
	sendTimedEmails("", "", "")

