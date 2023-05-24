from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CreatePollForm
from .models import Poll
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate

def uhome(request):
	if request.user.is_authenticated:
		return redirect("poll/uwelcome")
	else:
		if request.method=="POST":
			un=request.POST.get("un")
			pw=request.POST.get("pw")
			usr=authenticate(username=un, password=pw)
			if usr is None:
				return render(request, "poll/uhome.html",{"msg":"invalid username / password "})
			else:
				login(request, usr)
				return redirect("uwelcome")
		else:
			return render(request, "poll/uhome.html")

def usignup(request):
	if request.user.is_authenticated:
		return redirect("poll/uwelcome")
	else:
		if request.method=="POST":
			un=request.POST.get("un")
			pw1=request.POST.get("pw1")
			pw2=request.POST.get("pw2")
			if pw1==pw2:
				try:
					usr=User.objects.get(username=un)
					return render(request, "poll/usignup.html",{"msg":"user already registered"})
				except User.DoesNotExist:
					usr=User.objects.create_user(username=un, password=pw1)
					usr.save()
					return redirect("poll/uhome")
			else:
				return render(request,"poll/usignup.html", {"msg":"Passwords did not match"})
		else:
			return render(request, "poll/usignup.html")
def uwelcome(request):
	if request.user.is_authenticated:
		return render(request, "poll/uwelcome.html")
	else:
		return redirect("poll/uhome")
def ulogout(request):
	logout(request)
	return redirect("uhome")
def ucp(request):
	if request.user.is_authenticated:
		if request.method=="POST":
			un=request.POST.get("un")
			pw1=request.POST.get("pw1")
			pw2=request.POST.get("pw2")
			if pw1==pw2:
				try:
					usr=User.objects.get(username=request.user.username)
					usr.set_password(pw1)
					usr.save()
					return redirect("poll/uhome")
				except User.DoesNotExist:
					return render(request, "poll/ucp.html",{"msg":"user doesnot exist"})

			else:
				return render(request,"poll/ucp.html", {"msg":"Passwords did not match"})
		else:
			return render(request, "poll/ucp.html")
	else:
		return redirect("poll/home")

		
def home(request):
    polls = Poll.objects.all()
    context = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('poll/home')
    else:
        form = CreatePollForm()
    context = {
        'form' : form
    }
    return render(request, 'poll/create.html', context)


def vote(request, poll_id):
	poll = Poll.objects.get(pk=poll_id)
	if request.method == 'POST':
		selected_option = request.POST['poll']
		if selected_option == 'option1':
			poll.option_one_count += 1
		elif selected_option == 'option2':
			 poll.option_two_count += 1
		elif selected_option == 'option3':
			poll.option_three_count += 1
		else:
			return HttpResponse(400, 'Invalid form')

		poll.save()

		return redirect('results', poll.id)

	context = {
		'poll' : poll
	}
	return render(request, 'poll/vote.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)

def delete(request, poll_id):
	post = get_object_or_404(Poll,pk=poll_id)
	form = CreatePollForm(request.POST)
	context = {'post' : post}
	if request.user.is_superuser:
		return render(request, 'poll/delete.html')
		if request.method == 'GET':
			return render(request, 'poll/home.html',context)
		elif request.method == 'POST':	
			form.delete()
			messages.success(request,  'The post has been deleted successfully.')
			return redirect('poll/home')
	else:
		return render(request, 'poll/delete.html')
