from django.shortcuts import render
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

def lect_home(request):
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}
	return render(request, "Lecturer/lecturerHome.html", user_dict)

def lect_publish(request):
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}
	return render(request, "Lecturer/LecturerPublish.html", user_dict)

def lect_units(request):
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}
	return render(request, "Lecturer/LecturerUnits.html", user_dict)

@login_required
def user_logout(request):
    """
        Closes the current session of the user,
        and redirects them to the login page.

        Parameters
        ----------
        request: HTTP request object
            Contains the request type sent by the user.
    """
    logout(request)
    return HttpResponseRedirect(reverse('administrative:user_logout'))
