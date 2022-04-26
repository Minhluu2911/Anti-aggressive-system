from django.apps import AppConfig


adafruitData = {}
maxEmo = 100
maxWater = 4
client = [None]

class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'