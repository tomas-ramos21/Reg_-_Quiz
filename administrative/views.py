# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Render HTML pages for both static and dynamic types.
# Last Modified By: Tomas Ramos
# Last Modified Date: 23-03-2019

import csv
import io
import os
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from generic.utils import register_employee, register_student, find_user, register_room, register_building, find_room, find_building, register_units, register_courses, register_teaching_period, extract_info_student, extract_info_lecturer, edit_units
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from student.models import Student
from administrative.models import Employee, Teaching_Period
from generic.utils import get_admin_context, admin_attendance_csv, admin_space_csv
from generic.decorator import is_admin
from generic.graphs import admin_room_usage, admin_attendance_graph
from django.contrib import messages
from generic.statistics_generator import stat_generator, csv_transfer, room_usage_csv

@login_required
def admin_home(request):
	"""
		Renders administratives' staff home page.

		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)
	return render(request, 'administrative/admin_home.html', user_dict)

@login_required
def acc_management(request):
	"""
		Renders the account management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)
	return render(request, 'administrative/accountM.html', user_dict)

@login_required
def admin_stats(request):
	"""
		Handles request sent by the user when using the
		resource & attendance statistics page. 

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)
	return render(request, 'administrative/statistics.html', user_dict)

@login_required
def unit_management(request):
	"""
		Renders the unit management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)

	if request.method == 'GET':
		return render(request, 'administrative/unitsM.html', user_dict)

	if request.method == "POST" and 'units_file' in request.FILES:
		csv_file = request.FILES['units_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		status, msg = register_units(file_path)
		if status == False:
			messages.error(request, msg, extra_tags='alert-warning')
			return redirect('administrative:unit_management')
		else:
			messages.success(request, 'Units updated', extra_tags='alert-success')
			return redirect('administrative:unit_management')

	if request.method == "POST" and 'courses_file' in request.FILES:
		csv_file = request.FILES['courses_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		status, msg = register_courses(file_path)
		if status == False:
			messages.error(request, msg, extra_tags='alert-warning')
			return redirect('administrative:unit_management')
		else:
			messages.success(request, 'Courses updated', extra_tags='alert-success')
			return redirect('administrative:unit_management')

	if request.method == "POST" and 'add_rm_file' in request.FILES:
		csv_file = request.FILES['add_rm_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		status, msg = edit_units(file_path)
		if status == False:
			messages.error(request, msg, extra_tags='alert-warning')
			return redirect('administrative:unit_management')
		else:
			messages.success(request, 'Units of lecturers updated', extra_tags='alert-success')
			return redirect('administrative:unit_management')

	if request.method == "POST" and 'teaching_period_file' in request.FILES:
		csv_file = request.FILES['teaching_period_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		status, msg = register_teaching_period(file_path)
		if status == False:
			messages.error(request, msg, extra_tags='alert-warning')
			return redirect('administrative:unit_management')
		else:
			messages.success(request, 'Teaching periods updated', extra_tags='alert-success')
			return redirect('administrative:unit_management')

	return render(request, 'administrative/unitsM.html', user_dict)

@login_required
def space_management(request):
	"""
		Renders the space management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)

	# Re-render the page
	if request.method == "GET":
		return render(request, 'administrative/teachingspace.html', user_dict)

	# Process to obtain CSV - Rooms
	if request.method == "POST" and 'room_file' in request.FILES:
		csv_file = request.FILES['room_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		status, msg = register_room(file_path)
		if status == False:
			messages.error(request, msg, extra_tags='alert-warning')
			return redirect('administrative:space_management')
		else:
			messages.success(request, "Rooms updated", extra_tags='alert-success')
			return redirect('administrative:space_management')

	# Process to obtain CSV - Buildings
	if request.method == "POST" and 'building_file' in request.FILES:
		csv_file = request.FILES['building_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		status, msg = register_building(file_path)
		if status == False:
			messages.error(request, msg, extra_tags='alert-warning')
			return redirect('administrative:space_management')
		else:
			messages.success(request, "Buildings updated", extra_tags='alert-success')
			return redirect('administrative:space_management')

	# Process to find Rooms
	if request.method == "POST" and not request.POST.get('room_code') is None:
		room_code = request.POST.get('room_code')
		room = find_room(room_code)

	# Process to find Buildings
	if request.method == "POST" and not request.POST.get('building_code') is None:
		building_code = request.POST.get('building_code')
		building = find_building(building_code)

	return render(request, 'administrative/teachingspace.html', user_dict)

@login_required
def employee_creation(request):
	"""
		Handles request sent by the user when using the
		staff creation page. The page may be re-rendered or
		a file may be submitted.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)
	# Re-render the page
	if request.method == "GET":
		return render(request, 'administrative/lectAccAdd.html', user_dict)

	# Process to obtain CSV & create accounts
	if request.method == "POST" and 'files' in request.FILES:
		csv_file = request.FILES['files']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		status, msg = register_employee(file_path)
		if status == False:
			messages.error(request, msg, extra_tags='alert-warning')
			return redirect('administrative:employee_creation')
		else:
			messages.success(request, 'Employee records updated', extra_tags='alert-success')
			return redirect('administrative:employee_creation')

	return render(request, 'administrative/lectAccAdd.html', user_dict)

@login_required
def student_creation(request):
	"""
		Handles request sent by the user when using the
		student creation page. The page may be re-rendered or
		a file may be submitted.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)

	# Process to render the page
	if request.method == "GET":
		return render(request, 'administrative/stuAccAdd.html', user_dict)

	# Process to obtain CSV & create accounts
	if request.method == "POST":
		csv_file = request.FILES['files']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		status, msg = register_student(file_path)
		if status is False:
			messages.error(request, msg, extra_tags='alert-warning')
			return redirect('administrative:student_creation')
		else:
			messages.success(request, 'Student records updated', extra_tags='alert-success')
			return redirect('administrative:student_creation')

	return render(request, 'administrative/stuAccAdd.html', user_dict)

def attendance_stats(request):
	"""
		Handles request sent by the user when using the
		attendance statistics page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)
	user_dict['t_period'] = Teaching_Period.objects.all()
	if request.method == "POST":
		period = request.POST.get('period')
		granularity = request.POST.get('granularity')
		selection = request.POST.get('selection')

		if request.POST.get('submit'):
			graph = admin_attendance_graph(period, granularity, selection)
			if graph == False:
				messages.error(request, 'Information provided is wrong or the request object does not exists.', extra_tags='alert-warning')
				return redirect('administrative:attendance_stats')
			user_dict['graph'] = graph
			user_dict['period'] = period
			user_dict['granularity'] = granularity
			user_dict['selection'] = selection
			return render(request, 'administrative/statisticsAttendance.html', user_dict)
		elif request.POST.get('download') :
			response = admin_attendance_csv(period, granularity, selection)
			if response == False:
				messages.error(request, 'Information provided is wrong or the request object does not exists.', extra_tags='alert-warning')
				return redirect('administrative:attendance_stats')
			return response
	return render(request, 'administrative/statisticsAttendance.html', user_dict)

def space_stats(request):
	user = request.user
	user_dict = get_admin_context(user)
	user_dict['t_period'] = Teaching_Period.objects.all()

	if request.method == "POST":
		period = request.POST.get('period')
		selection = request.POST.get('room_code')
		if request.POST.get('submit') :
			graph = admin_room_usage(period, selection)
			if graph is None:
				messages.error(request, 'Information provided is wrong or the request object does not exists.', extra_tags='alert-warning')
				return redirect('administrative:space_stats')
			user_dict['graph'] = graph
			user_dict['period'] = period
			user_dict['selection'] = selection
			return render(request, 'administrative/statisticsUsage.html', user_dict)
		elif request.POST.get('download') :
			response = admin_space_csv(period, selection)
			if response == False:
				messages.error(request, 'Information provided is wrong or the request object does not exists.', extra_tags='alert-warning')
				return redirect('administrative:space_stats')
			else:
				return response
		"""
		messages.success(request, 'Downloaded csv successfully', extra_tags='alert-success')
		return render(request, 'administrative/statisticsUsage.html', user_dict)
		"""
	return render(request, 'administrative/statisticsUsage.html', user_dict)

def user_view(request):
	"""
		Renders user view

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	username = request.POST.get('search_user')
	searched_user = User.objects.filter(username=username).first()
	user_dict = get_admin_context(user)

	if searched_user is None:
		messages.error(request, 'User ID: ' + username + ' was not found', extra_tags='alert-warning')
		return redirect('administrative:user_view')

	student = Student.objects.filter(user=searched_user).first()
	lecturer = Employee.objects.filter(user=searched_user).first()

	classes = None
	units = None
	courses = None
	user_object = None
	
	if student is not None:
		classes, courses, units = extract_info_student(student)
		user_object = student
	else:
		classes, units = extract_info_lecturer(lecturer)
		user_object = lecturer

	user_dict['user_object'] = user_object
	user_dict['classes'] = classes
	user_dict['units'] = units
	user_dict['courses'] = courses

	return render(request, 'administrative/userView.html', user_dict)

@login_required
def admin_error(request):
	"""
		Renders error page

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_admin_context(user)
	return render(request, 'administrative/error.html', user_dict)

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
