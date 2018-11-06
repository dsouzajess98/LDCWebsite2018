from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import subscriber,books,receipt,comments
from django.contrib.auth.decorators import login_required,user_passes_test
import datetime
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
#from registration.backends.simple.views import RegistrationView





# Create your views here.
def index(request):
	return render(request,'base/index.html')

def meettheteam(request):
	return render(request,'base/TheClub.html')

# def signup(request):
# 	return render(request,'base/Signup.html')
#
# def login(request):
# 	return render(request,'base/Login.html')
#
def terms(request):
	return render(request,'base/terms.html')

def _404(request):
	return render(request,'base/terms.html')

def is_subscribed(user):
	present_user = subscriber.objects.get(user = user)
	if present_user.is_subscribed:
		return True
	else:
		return False



@login_required
def tables(request):
	book = books.objects.all()
	present_user = subscriber.objects.get(user = request.user)

	messages.add_message(request,messages.INFO,'Books will be available ONLY after you have been subscribed by the Admin.')
	context = { 'book' : book , 'name' : present_user.user.username, 'pass': present_user.is_subscribed}
	return render(request,'book/tables.html',context)

@login_required
def profile(request):
	# messages.add_message(request,messages.INFO,'Welcome to your shitty profile')
	try:
		present_user = subscriber.objects.get(user = request.user)
	except:
		sub = subscriber.objects.create(user = request.user)
		sub.save()
	present_user = subscriber.objects.get(user = request.user)
	if present_user.is_subscribed:
		try:
			cur_receipt  = receipt.objects.filter(subscriber = present_user).get(status='I')
		except:
			cur_receipt = None
		try:
			pb_receipt = receipt.objects.filter(subscriber = present_user).get(status = 'PB')
		except:
			pb_receipt = None
		if cur_receipt:
			dateofissue  = cur_receipt.date
			days = datetime.date.today() - dateofissue
			if(days.days>21):
				flag = 1
				days = 21 - days.days
				days = abs(days)
				if(days < 7):
					fine = 10
				else:
					fine  = 10 + ((days / 7)*20)
			else:
				fine = 0
				flag = 0
				days = days.days
			flag1 = 0
			if pb_receipt is None:
				pb_book_name = 'None'
				pbbookid = ''
			else:
				pb_book_name = pb_receipt.book.name
				pbbookid = pb_receipt.book.bookid

			days = abs(days)
			context = {'name' : present_user.user.username , 'book' : cur_receipt.book.name , 'date' : dateofissue , 'days' : days , 'flag' : flag , 'fine' : fine , 'sub' : flag1 ,'pb' : pb_book_name , 'id' : pbbookid }
		else:
			flag1 = 2
			if pb_receipt is None:
				pb_book_name = 'None'
				context = {'name' : present_user.user.username , 'sub' : flag1 ,'pb' : pb_book_name}
			else:
				pb_book_name = pb_receipt.book.name
				pbbookid = pb_receipt.book.bookid
				context = {'name' : present_user.user.username , 'sub' : flag1 ,'pb' : pb_book_name , 'id' : pbbookid}

	else:
		flag1 = 1
		messages.add_message(request,messages.INFO,'You are not subscribed yet! Please wait for the Admin to approve you.')
		context = {'name' : present_user.user.username , 'sub' : flag1,'pb' : 'None' }
	return render(request,'book/profile.html',context)


@login_required
@user_passes_test(is_subscribed,login_url = '/')
def preregister(request,b_id):
	present_user = subscriber.objects.get(user = request.user)
	r = receipt.objects.filter(subscriber = present_user).filter(status='PB')
	b = books.objects.get(bookid = b_id)
	if not r and b.is_available:

		b.is_available = False
		b.save()
		rec = receipt.objects.create(subscriber = present_user, book = b , status = 'PB' )
		rec.save()
	else:
		messages.add_message(request,messages.INFO,'You are not allowed to prebook more than 1 book')
	return redirect(profile)

@user_passes_test(is_subscribed,login_url = '/')
@login_required
def done_preregister(request):
	return HttpResponse("Bleh")

def book(request,book_id):
	book = books.objects.get(bookid = book_id)
	present_user = subscriber.objects.get(user = request.user)

	# messages.add_message(request,messages.INFO,'Books will be available ONLY after you have been subscribed by the Admin.')
	# context = { 'book' : book , 'name' : present_user.user.username, 'pass': present_user.is_subscribed}

	comms = comments.objects.filter(book = book)
	context = {'name' : book.name , 'des' : book.des , 'author' : book.author,'id' : book_id , 'comments' : comms , 'available' : book.is_available, 'pass': present_user.is_subscribed}
	return render(request,'book/bookpage.html',context)

@user_passes_test(is_subscribed,login_url = '/')
@login_required
def post_comment(request,book_id):
	bookie =  books.objects.get(bookid = book_id)
	present_user = subscriber.objects.get(user = request.user)
	if request.method == 'POST':
		comm = request.POST['commentbox']
	comment =  comments.objects.create(subscriber = present_user ,book =  bookie,comment = comm )
	comment.save()
	return redirect(book,book_id = book_id)

@login_required
def setting(request):
	present_user = subscriber.objects.get(user = request.user)
	context = {'user' : present_user}
	return render(request,'book/setting.html',context)

@login_required
def update_settings(request):
	sub = subscriber.objects.get(user = request.user)
	if request.method == 'POST':
		f_name = request.POST['f_name']
		l_name = request.POST['l_name']
		p_no = request.POST['p_no']
		regno = request.POST['regno']
		hostel_name = request.POST['hostel']
		room_no = request.POST['room']
		if len(regno)>1 and len(p_no)>1:
			sub.is_complete = True
		sub.user.first_name = f_name
		sub.user.last_name = l_name
		sub.pno = p_no
		sub.reg_no = regno
		sub.hostel = hostel_name
		sub.room = room_no
		sub.user.save()
		sub.save()

	messages.add_message(request,messages.INFO,'You have successfully updated your details! Please wait for the Admin to approve you.')
	return redirect(setting)

def cancelprebook(request,b_id):
	present_user = subscriber.objects.get(user = request.user)
	r = receipt.objects.filter(subscriber = present_user).filter(status='PB')
	r.delete()
	b = books.objects.get(bookid = b_id)
	b.is_available = True
	b.save()
	return redirect(profile)
