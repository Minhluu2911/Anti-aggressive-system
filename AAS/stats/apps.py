from django.apps import AppConfig


adafruitData = {
    'emotionData': [],
    'waterData': [],
}
maxEmo = 100
maxWater = 4
speed = [0]
client = [None]

class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'