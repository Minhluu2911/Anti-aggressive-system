from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.defaulttags import register

from datetime import date
import calendar

from .models import EmotionData

from .apps import adafruitData, speed, client, maxEmo, maxWater


def toMinuteData(data, func): # 1 update / 10 secs
	return [func(data[i:i+6]) for i in range(0, len(data), 6)]

@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]

def mystat(request):
	#time.sleep(5) # => long polling
	global adafruitData

	return render(request, 'stats/index.html', {
		'today': date.today(),
		'username': request.user.username,
		'maxEmo': maxEmo,
		'maxWater': maxWater,
		'overallScore': EmotionData.objects.filter(user=request.user)[0].current_score,
		'avgEmo': round(maxEmo * (lambda xs : sum(xs) / len(xs) if xs else 1)(adafruitData['emotionData']), 2),
		'sumWater': round(maxWater * (lambda xs : sum(xs))(adafruitData['waterData']), 2),
		'emotion': str(toMinuteData(adafruitData['emotionData'], lambda xs : sum(xs) / len(xs))),
		'water': str(toMinuteData(adafruitData['waterData'], lambda xs : sum(xs))),
		})

def export_data(request):
	emotionDataSet = EmotionData.objects.filter(user=request.user)
	if not emotionDataSet:
		emotionData = EmotionData(
			user=request.user,
			current_score=maxEmo * (lambda xs : sum(xs) / len(xs) if xs else 1)(adafruitData['emotionData']),
			number_of_days=1,
			)
	else:
		emotionData = emotionDataSet[0]
		emotionData.current_score = (emotionData.current_score * emotionData.number_of_days + maxEmo * (lambda xs : sum(xs) / len(xs) if xs else 1)(adafruitData['emotionData'])) / (emotionData.number_of_days + 1)
		emotionData.number_of_days += 1

	emotionData.save()
	return redirect(reverse('stats:mystat'))

def leaderboard(request):
	return render(request, 'stats/tables.html', {
		'username': request.user.username,
		'emotionData': EmotionData.objects.order_by('-current_score'),
		})

def leaderboard_admin(request):
	return render(request, 'stats/tables-admin.html', {})