# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Define functions providing extra utility to the administrative app.
# Last Modified By: Madyarini
# Last Modified Date: 20-03-2019

import os
import csv
import random
from django.http import HttpResponseRedirect, HttpResponse
from student.models import Student
from lecturer.models import Question
from administrative.models import Building, Room, Employee, Unit, Course, Teaching_Period
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from typing import Dict, Tuple


def register_employee(csv_path: str) -> None:
    """
        Registers lecturers in the platform.

        Iterates over the rows of a CSV file
        collecting the information to be used
        for the account creation.

        Parameters
        ----------
        csv_path: str
            String containing the path to the
            file.

        TODO
        ----------
        1. Function do check the information
        used during creation is accurate.
    """

    columns = ['id',
               'password',
               'first_name',
               'last_name',
               'email',
               'department',
               'position']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):  # For each row
            if idx != 0:                    # If row isn't the header
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                user = User()
                user.set_password(crt_dict['password'])
                user.username = crt_dict['id']
                user.first_name = crt_dict['first_name']
                user.last_name = crt_dict['last_name']
                user.email = crt_dict['email']
                user.save()
                employee = Employee(user=user,
                                    dpt=crt_dict['department'],
                                    pstn=crt_dict['position'])
                employee.save()

def register_student(csv_path: str) -> None:
    """
        Registers students in the platform.

        Iterates over the rows of a CSV file
        collecting the information to be used
        for the account creation.

        Parameters
        ----------
        csv_path: str
            String containing the path to the
            file.

        TODO
        ----------
        1. Function do check the information
        used during creation is accurate.
    """

    columns = ['id',
               'password',
               'first_name',
               'last_name',
               'email']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                user = User()
                user.set_password(crt_dict['password'])
                user.username = crt_dict['id']
                user.first_name = crt_dict['first_name']
                user.last_name = crt_dict['last_name']
                user.email = crt_dict['email']
                user.save()
                student = Student(user=user)
                student.save()

def get_context(user) -> Dict:
    context_dict = {'name_header' : user.first_name,
                    'name_menu'   : user.first_name + ' ' + user.last_name }
    return context_dict

def find_user(username:str) -> Tuple:

    # Find user object
    user = User.objects.filter(username=username).first()
    # If user doesn't exist
    if user is None:
        return (None, None)

    # Find student object
    student	= Student.objects.filter(user=user).first()
    # If student exists
    if not student is None:
        return (student, 'student')

    # Find employee object
    employee = Employee.objects.filter(user=user).first()
    # if employee exists
    if not student is None:
        return (employee, 'employee')

def register_room(csv_path: str) -> None:

    columns = ['id',
               'building_code',
               'level',
               'capacity']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                building = Building.objects.filter(code=crt_dict['building_code']).first()
                room = Room(id=crt_dict['id'],
                            bd_code=building,
                            level=crt_dict['level'],
                            capacity=crt_dict['capacity'])
                room.save()

def register_building(csv_path:str) -> None:

    columns = ['code','name']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                building = Building(code=crt_dict['code'], name=crt_dict['name'])
                building.save()

def register_units(csv_path:str) -> None:

    columns = ['code','title','credits','image']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                unit = Unit(code=crt_dict['code'],
                            title=crt_dict['title'],
                            credits=crt_dict['credits'],
                            image=crt_dict['image'])
                unit.save()

def register_courses(csv_path: str) -> None:

    columns = ['id', 'title', 'school']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                course = Course(id=crt_dict['id'],
                                title=crt_dict['title'],
                                school=crt_dict['school'])
                course.save()

def register_teaching_period(csv_path: str) -> None:
    columns = ['id', 'name', 'start_date', 'end_date']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)
        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                teaching_period = Teaching_Period(id=crt_dict['id'],
                                                  name=crt_dict['name'],
                                                  st_date=crt_dict['start_date'],
                                                  en_date=crt_dict['end_date'])
                teaching_period.save()

def register_questions(csv_path: str) -> None:
    columns = ['unit',
               'staff_id',
               'question',
               'answer_1',
               'answer_2',
               'answer_3',
               'answer_4']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)
        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                unit = Unit.objects.filter(code=crt_dict['unit']).first()
                user = User.objects.filter(username=crt_dict['staff_id']).first()
                lecturer = Employee.objects.filter(user=user).first()
                question = Question(text=crt_dict['question'],
                                    ans_1=crt_dict['answer_1'],
                                    ans_2=crt_dict['answer_2'],
                                    ans_3=crt_dict['answer_3'],
                                    ans_4=crt_dict['answer_4'],
                                    unit_id=unit,
                                    staff_id=lecturer)
                question.save()

def find_room(room_code):
    return Room.objects.filter(id=room_code).first()

def find_building(building_code):
    return Building.objects.filter(code=building_code).first()

def generate_random_code():
    # Generates random code for questions
    # Number has always 9 digits
    # So its easy to display like this      999-666-888
    return random.randint(100000000, 999999999)
