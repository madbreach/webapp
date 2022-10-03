# misc packages
import datetime
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
# models
from .models import JoinLink
from .models import Pronoun
from .models import UserSection
from .models import Section
from .models import Attendance




# Create your views here.
def index(request):
    joinLink = JoinLink.objects.get(link=request.GET['t'])
    curr_user = joinLink.user
    template = loader.get_template('UtahPrideCenter/index.html')
    context = {
        'display_name': curr_user.display_name,
        'first_name': curr_user.first_name,
        'last_name': curr_user.last_name,
        'join_token': joinLink.link,
    }
    return render(request, "UtahPrideCenter/index.html", context)

def check_in(request):
    joinLink = JoinLink.objects.get(link=request.GET['t'])
    curr_user = joinLink.user
    context = {
        'join_link': joinLink.link,
        'user_sections': list(UserSection.objects.filter(user=curr_user))
    }
    return render(request, "UtahPrideCenter/checkin.html", context)

def confirmation(request):
    joinLink = JoinLink.objects.get(link=request.POST['token'])
    curr_user = joinLink.user
    section = Section.objects.get(pk=request.POST['section'])
    attendance = Attendance.objects.create(user=curr_user, section=section, check_in_time=datetime)
    user_section = UserSection.objects.get(user=curr_user, section=section)
    context = {
        'join_link': joinLink.link,
        'zoom_link': section.zoom_link
    }
    return render(request, "UtahPrideCenter/confirmation.html", context)

def edit_info(request):
    joinLink = JoinLink.objects.get(link=request.GET['t'])
    curr_user = joinLink.user
    context = {
        'token': joinLink.link,
        'first_name': curr_user.first_name,
        'last_name': curr_user.last_name,
        'display_name': curr_user.display_name,
        'user_pronouns': curr_user.pronouns,
        'user_specified': curr_user.specified_pronouns,
        'pronouns': Pronoun.objects.all(),
    }
    return render(request, "UtahPrideCenter/editinfo.html", context)

# update pronouns or display name
def update(request):
    joinLink = JoinLink.objects.get(link=request.POST['token'])
    curr_user = joinLink.user

    curr_user.display_name = request.POST['fname']
    curr_user.pronouns = Pronoun.objects.get(pk=request.POST['pronouns'])
    curr_user.specified_pronouns = request.POST['custom']
    curr_user.save()

    return HttpResponseRedirect(reverse('EditInfo') + "?t=" + joinLink.link)