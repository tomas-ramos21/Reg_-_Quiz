from django.db import models
from administrative.models import Course
from lecturer.models import Published_Question, Class, Teaching_Day
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone

class Student(models.Model):

    """
        Django's Model to represent the Student
		class in the MySQL Database.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', default='')
    s_class = models.ManyToManyField(Class, blank=True)                 # Many Students to Many Classes
    s_course= models.ManyToManyField(Course)                # Many Students to Many Courses

class Answer(models.Model):

	"""
		Django's Model to represent the Answer
		class in the MySQL.
	"""

	answers = (
		('answer_1', 'Answer 1'),
		('answer_2', 'Answer 2'),
		('answer_3', 'Answer 3'),
		('answer_4', 'Answer 4'),
	)
	
	s_id		= models.ForeignKey(Student, on_delete=models.PROTECT)		# Student ID
	q_id		= models.ForeignKey(Published_Question, on_delete=models.PROTECT)		# Question ID
	teach_day	= models.ForeignKey(Teaching_Day, on_delete=models.PROTECT)	# Teaching Day ID
	ans			= models.CharField(max_length=8, choices=answers)				# Answer Option
	tm_stmp		= models.DateTimeField(editable=False)					# Time Stamp
	ip_addr		= models.CharField(max_length=15)				# IP Type
	
	def save(self, *args, **kwargs):
		if not self.tm_stmp:
			self.tm_stmp = datetime.now(timezone.utc)
		return super(Answer, self).save(*args, **kwargs)
		
	def __str__(self):
		return self.s_id.user.username + ' ' + str(self.q_id.code) + ' ' + str(self.teach_day.date_td) + ' ' + self.ans + ' ' + str(self.tm_stmp) + self.q_id.question.topic_id.unit_id.code 