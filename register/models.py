from django.db import models

#Create Your Models Here.
class User(models.Model):
	#Public Member Variables.
	currentName = models.CharField(max_length=100)
	currentChatDataBasePath = models.CharField()
	prevLastVisitedTime = models.DateField()

	#Plural Meta Data For User Class:
	class Meta:
		verbose_name_plural = 'Users'

	#String Representation For Users:
	def __str__(self):
		return self.currentName
