from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, get_user_model
# Create your views here.


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserLoginForm, take_quiz
from .models import Question, Answer, Level, UserInput

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

def ques_list(request):
	print request.user.level_id
	user_level = request.user.level_id
	q = Question.objects.filter(level_id = user_level)
	question_list = q.prefetch_related('qus')
	page = request.GET.get('page', 1)
	paginator = Paginator(question_list, 1)
	try:
		questions = paginator.page(page)
		print questions
	except PageNotAnInteger:
		questions = paginator.page(1)
		print questions
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)
		print questions
	return render(request, "accounts/quiz.html", {"questions":questions})


def option_list(request):
	pass



def take_quiz(request):
	user_level = 2
	print user_level
	level = Level.objects.filter(id = user_level)
	for question in level:
		fields = {}
		questions = question.question_set.all()
		for answer in questions:
			field_name = "question_%d" %question.id
			choices = []
			for a in answer.answer_set.all():
				choices.append((a.id, a.answer_content,))
			print choices
	# return render(request, "accounts/quiz.html", {"question_list":question_list, 
	# 											  "choice_list": choice_list})

	return HttpResponseRedirect("/login")
	#return type('TakeQuizForm', (forms.BaseForm,), {'base_fields': fields})


def save_answer(request):
	#u = UserInput.objects.filter(User)
	user_ans = request.POST.get('answer')
	print "=="*30
	print user_ans
	print "=="*30
	a = Answer.objects.filter(id=user_ans).values_list('is_correct')[0][0]
	if a:
		x = 1
	else:
		x = 0
	b = UserInput(user_id=request.user.id, user_answer=user_ans, score=x)
	b.save()
	return HttpResponseRedirect("/")


def get_score(request):
	l = request.user.level_id
	
	
