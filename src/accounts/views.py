from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseForbidden
from django.contrib.auth import login, logout, get_user_model
# Create your views here.

from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import send_mail
from .forms import UserLoginForm, take_quiz, ImageUploadForm
from .models import Question, Answer, Level, UserInput, ImageDescModel
from itertools import chain

User = get_user_model()

# User Home Page
def home(request):
	if request.user.is_authenticated():

		return render(request, "accounts/home.html", {})
	else:
		return HttpResponseRedirect("/login")

#User Login
def user_login(request, *args, **kwargs):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		user_obj = form.cleaned_data.get('user_obj')
		login(request, user_obj)
		return HttpResponseRedirect("/")
	return render(request, "accounts/login.html", {"form": form})


# User Logout
def user_logout(request):
	logout(request)
	return HttpResponseRedirect("/login")


# To get the list if Questions in the particular level along with options
def ques_list(request, level_id):
	a = list(UserInput.objects.filter(
		user_id=request.user.id, level_id=level_id).values_list('question_id'))
	print a
	x = list(chain.from_iterable(a))
	print x
	q = Question.objects.filter(level_id=level_id).exclude(id__in=x).order_by('id')
	print q
	if not q:
		print "questions over"
		text = "You have attempted all the questions"
		return render(request, "accounts/quiz_over.html", {"text":text})

	else:	
		question_list = q.prefetch_related('qus')
		print question_list

		page = request.GET.get('page')
		print page
		paginator = Paginator(question_list, 1)
		print paginator
		try:
			questions = paginator.page(page)
			print "try"
		except PageNotAnInteger:
			questions = paginator.page(1)
			print "except"
		except EmptyPage:
			questions = paginator.page(paginator.num_pages)
			print "empty page"
		print questions
		return render(request, "accounts/quiz.html", {"questions":questions})


# Save Answers to the database
def save_answer(request):
	user = request.user.id
	user_ans = request.POST.get('answer')
	user_ques = request.POST.get('ques')
	user_level = request.POST.get('level')

	a = Answer.objects.filter(id=user_ans).values_list('is_correct')[0][0]
	if a:
		x = 1
	else:
		x = 0
	obj, created = UserInput.objects.update_or_create(
					user_id=user, question_id=user_ques,
					defaults={'score': x,
							'level_id':user_level,
							'user_answer':user_ans})
	return HttpResponseRedirect("/")


#Calculate Score for User and show the status of level completion.
def get_score(request):
	user = request.user.id
	total_ques_1 = Question.objects.filter(level_id=1)
	total_ques_2 = Question.objects.filter(level_id=2)
	total_ques_3 = Question.objects.filter(level_id=3)
	prac_test_exist_1 = ImageDescModel.objects.filter(user_id=user, level_id=1).exists()
	prac_test_exist_2 = ImageDescModel.objects.filter(user_id=user, level_id=2).exists()
	prac_test_exist_3 = ImageDescModel.objects.filter(user_id=user, level_id=3).exists()
	user_level_1 = User.objects.filter(id=user).values('level_one')[0]['level_one']
	user_level_2 = User.objects.filter(id=user).values('level_two')[0]['level_two']
	user_level_3 = User.objects.filter(id=user).values('level_three')[0]['level_three']

	s1 = UserInput.objects.filter(
		user_id=user, level_id=1
		).aggregate(Sum('score'))['score__sum']
	s2 = UserInput.objects.filter(
		user_id=user, level_id=2
		).aggregate(Sum('score'))['score__sum']
	s3 = UserInput.objects.filter(
		user_id=user, level_id=3
		).aggregate(Sum('score'))['score__sum']
	print user
	print s1,s2,s3	
	print prac_test_exist_1, prac_test_exist_2, prac_test_exist_3

	if prac_test_exist_1 == True:
		p1 = "Finished"
	else:
		p1 = "Not Finished"

	if prac_test_exist_2 == True:
		p2 = "Finished"
	else:
		p2 = "Not Finished"
	if prac_test_exist_3 == True:
		p3 = "Finished"
	else:
		p3 = "Not Finished"

	if s1 == total_ques_1 and prac_test_exist_1==True:
		l1 = "Completed"
	else:
		l1 = "Not Completed"
	if s2 == total_ques_2 and prac_test_exist_2==True:
		l2 = "Completed"
	else:
		l2 = "Not Completed"
	if s3 == total_ques_2 and prac_test_exist_3==True:
		l3 = "Completed"
	else:
		l3 = "Not Completed"

	context = {"s1":s1, "s2":s2, "s3":s3,
				"p1":p1, "p2":p2, "p3":p3,
				"l1":l1, "l2":l2, "l3":l3,
				"user_level_1":user_level_1,
				"user_level_2":user_level_2,
				"user_level_3":user_level_3,
				}
				
	return render(request, "accounts/score.html", context)


# Select Quiz or Practical Test
def select_exam(request, level_id):
	level = level_id
	print level
	return render(request, "accounts/select_test.html", {"level":level}) 


# Upload picture and add description for Practical Test
def practical_test(request, level_id):
	level = level_id
	print level
	form = ImageUploadForm()
	return render(request, "accounts/practical_test.html", {"level":level, "form":form})


# Save the uploaded picture and desription to the database
def upload_pic(request,level_id):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            obj, created = ImageDescModel.objects.get_or_create(
					user_id=request.user.id, level_id=level_id,
					defaults={'description': description,
							'image':image,})
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')


# If User wants to retake level
def retake_level(request, level_id):
	level = level_id
	user = request.user.id
	UserInput.objects.filter(user_id=user, level_id=level).delete()
	return HttpResponseRedirect("/qlist/" + level)


# Will change user level in User table 
# and send email to user
def level_complete(request):
	clickval = request.POST.get('clicked_value')
	print clickval
	if clickval == '1':
		User.objects.filter(id=request.user.id).update(level_one='Y')
	elif clickval == '2':
		User.objects.filter(id=request.user.id).update(level_two='Y')
	else:
		User.objects.filter(id=request.user.id).update(level_three='Y')

	print settings.NOTIFY_LEVEL_COMPLETE
	send_mail(
		'Level %s - Completed' % (clickval),
		'Congratulations on finishing this level.',
		'staradhish@gmail.com',
		[settings.NOTIFY_LEVEL_COMPLETE],
		fail_silently=False,
		)
	return render(request, "accounts/score.html", {})


