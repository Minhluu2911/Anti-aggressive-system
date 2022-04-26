from django.db import models

class EmotionData(models.Model):
	user = models.ForeignKey('register.User', on_delete=models.CASCADE)
	current_score = models.FloatField()
	number_of_days = models.IntegerField()