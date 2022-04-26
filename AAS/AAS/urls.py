from django.contrib import admin
from django.urls import include, path

urlpatterns = [
	path('', include('stats.urls')),
	path('', include('homepage.urls')),
	path('', include('register.urls')),
    path('admin/', admin.site.urls),
]
