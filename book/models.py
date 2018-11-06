from __future__ import unicode_literals

from django.contrib.auth.models import User

from django.db import models
import datetime as d
from datetime import datetime

# Create your models here.

class subscriber(models.Model):
	user = models.OneToOneField(User,on_delete = models.CASCADE)
	is_subscribed =  models.BooleanField(default=False)
	is_complete =  models.BooleanField(default=False)

	pno = models.IntegerField(default = None,null=True)
	reg_no = models.IntegerField(default = None,null = True)
	hostel = models.CharField(max_length=10,null=True)
	room = models.CharField(max_length=10,null=True)

	def __unicode__(self):
		return self.user.username

class books(models.Model):
	name = models.CharField(max_length=60)
	author = models.CharField(max_length=60 ,default = 'author')

	des = models.CharField(max_length=600)
	bookid = models.CharField(max_length = 15)
	is_available = models.BooleanField(default = True)
	def __unicode__(self):
		return self.name

class receipt(models.Model):
	subscriber = models.ForeignKey(subscriber)
	book = models.ForeignKey(books)

	prebooked = 'PB'
	Issued = 'I'
	Returned = 'R'
	book_status_choices = (
        (Returned, 'Returned'),
        (prebooked, 'Pre-booked'),
        (Issued, 'Issued'),
    )
	status = models.CharField(max_length = 2, choices=book_status_choices,default=prebooked)
	date = models.DateField(default = d.date.today)
	def __unicode__(self):
		return str(self.subscriber.user.username + self.book.name + self.status)

class comments(models.Model):
	subscriber = models.ForeignKey(subscriber)
	book = models.ForeignKey(books)
	comment = models.CharField(max_length = 500 )
	time = models.DateTimeField(default = datetime.now)
