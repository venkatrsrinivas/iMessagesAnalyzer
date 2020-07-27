from django.db import models

#Create Your Models Here.
class User(models.Model):
	#Public Member Variables.
	currentEmail = models.EmailField()
	currentName = models.CharField(max_length=100)
	currentPathToRead = models.TextField()
	currentPathToWrite = models.TextField()
	prevComputeIndex = models.IntegerField()

	#Plural Meta Data For User Class:
	class Meta:
		verbose_name_plural = 'Users'

	#String Representation For Users:
	def __str__(self):
		return self.currentName;
