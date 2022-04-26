from django.shortcuts import render

def home(request):
	user = request.user
	if user.is_authenticated:
		return render(request, 'homepage/homepage-user.html', {
			'username': user.username,
			})
	else:
		return render(request, 'homepage/homepage-guest.html', {})

def home_admin(request):
	return render(request, 'homepage/homepage-admin.html', {})