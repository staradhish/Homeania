from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseForbidden
from django.contrib.auth import login, logout, get_user_model
# Create your views here.

from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserLoginForm, take_quiz, ImageUploadForm
from .models import Question, Answer, Level, UserInput, ImageDescModel
from itertools import chain

User = get_user_model()

def home(request):
	if request.user.is_authenticated():
		print request.user.level_id
		return render(request, "accounts/home.html", {})
	else:
		return HttpResponseRedirect("/login")


def user_login(request, *args, **kwargs):
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		user_obj = form.cleaned_data.get('user_obj')
		login(request, user_obj)
		return HttpResponseRedirect("/")
	return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
	logout(request)
	return HttpResponseRedirect("/login")


"""def ques_list(request):
	user_level = request.user.level_id
	question_list = Question.objects.filter(level_id = user_level)
	for question in question_list.values():
		x = question['id']
	# x = 1
		choices = []
		print question
		# for a in question.answer_set.all():
		# 	choices.append(a)
		# 	print choices
		choice_list = Answer.objects.filter(question_id = x)

	# page = request.GET.get('page', 1)
	# paginator = Paginator(question_list, 1)
	# try:
	# 	questions = paginator.page(page)
	# except PageNotAnInteger:
	# 	questions = paginator.page(1)
	# except EmptyPage:
	# 	questions = paginator.page(paginator.num_pages)

	return render(request, "accounts/quiz.html", {"question_list":question_list, 
												  "choice_list": choice_list})
"""

# def ques_list_old(request, level_id):
# 	print level_id
# 	#print request.user.level_id
# 	user_level = level_id
# 	q = Question.objects.filter(level_id = user_level)
# 	question_list = q.prefetch_related('qus')
# 	print question_list
# 	page = request.GET.get('page', 1)
# 	paginator = Paginator(question_list, 1)
# 	try:
# 		questions = paginator.page(page)
# 	except PageNotAnInteger:
# 		questions = paginator.page(1)
# 	except EmptyPage:
# 		questions = paginator.page(paginator.num_pages)
# 	return render(request, "accounts/quiz.html", {"questions":questions})


def ques_list(request, level_id):
	a = list(UserInput.objects.filter(
		user_id=request.user.id, level_id=level_id).values_list('question_id'))
	x = list(chain.from_iterable(a))
	q = Question.objects.filter(level_id=level_id).exclude(id__in=x)

	question_list = q.prefetch_related('qus')
	print question_list

	page = request.GET.get('page', 1)
	paginator = Paginator(question_list, 1)
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		questions = paginator.page(1)
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)
	return render(request, "accounts/quiz.html", {"questions":questions})

# def take_quiz(request):
# 	user_level = 2
# 	print user_level
# 	level = Level.objects.filter(id = user_level)
# 	for question in level:
# 		fields = {}
# 		questions = question.question_set.all()
# 		for answer in questions:
# 			field_name = "question_%d" %question.id
# 			choices = []
# 			for a in answer.answer_set.all():
# 				choices.append((a.id, a.answer_content,))
# 			print choices
# 	# return render(request, "accounts/quiz.html", {"question_list":question_list, 
# 	# 											  "choice_list": choice_list})

# 	return HttpResponseRedirect("/login")
# 	#return type('TakeQuizForm', (forms.BaseForm,), {'base_fields': fields})


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

	print "=="*30
	print user, user_level, user_ques, user_ans, x
	print "=="*30
	obj, created = UserInput.objects.update_or_create(
					user_id=user, question_id=user_ques,
					defaults={'score': x,
							'level_id':user_level,
							'user_answer':user_ans})
	print "=="*30
	print obj, created
	print "=="*30

	return HttpResponseRedirect("/")


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
	if s3 == total_ques_3 and prac_test_exist_3==True:
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


def select_exam(request, level_id):
	level = level_id
	print level
	return render(request, "accounts/select_test.html", {"level":level}) 


def practical_test(request, level_id):
	level = level_id
	print level
	form = ImageUploadForm()
	return render(request, "accounts/practical_test.html", {"level":level, "form":form})

# Will change user level in User table 
# and send email to user
def level_complete(request):
	clickval = request.POST.get('clicked_value')
	print clickval
	User.objects.filter(id=request.user.id).update(level_one='Y')
	return render(request, "accounts/score.html", {})


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

