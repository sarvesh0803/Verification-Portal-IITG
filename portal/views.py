# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,AnonymousUser
from django.shortcuts import HttpResponseRedirect,HttpResponse
from .models import Profile,type1,type2,team_detail,request_progress,path,record_progress,team_approval_progress,record_team_progress
from django.core.exceptions import ObjectDoesNotExist
from . import models
# Create your views here.




#......................................................................................................................#
#view for login from webmail

def get_user(webmail):
    try:
        return Profile.objects.get(webmail=webmail)
    except ObjectDoesNotExist:
        return None


def login_page(request):
    if request.user.is_authenticated():
        q= Profile.objects.get(user= request.user)
        webmail = q.webmail
        list1 = type1.objects.all().values_list('webmail', flat=True)
        list2 = type2.objects.all().values_list('webmail', flat=True)
        for obj in list1:
            if webmail == obj:
                return HttpResponseRedirect('/portal/profile1')
        for obj in list2:
            if webmail == obj:
                return HttpResponseRedirect('/portal/profile2')
        return HttpResponseRedirect('/portal/profile3')
    else:
        return render(request,'portal/login.html')



def login_view(request):
    if request.POST:
        webmail = request.POST['webmail']
        password = request.POST['password']
        username = get_user(webmail)
        if username is not None:
            user = authenticate(username = username , password= password)
            if user is not None:
                login(request,user)
                q = User.objects.get(username=username)
                list1 = type1.objects.all().values_list('webmail', flat=True)
                list2 = type2.objects.all().values_list('webmail', flat=True)
                for obj in list1:
                    if webmail == obj:
                        return render(request,'portal/profile1.html',{'username' : username})
                for obj in list2:
                    if webmail == obj:
                        return HttpResponseRedirect('/portal/profile2')
                return HttpResponseRedirect('/portal/profile3')
        else:
            return HttpResponse( 'webmail or password is wrong')
    else:
        return HttpResponseRedirect('/portal/login_page/')
    return HttpResponseRedirect('/portal/login_page/')

#......................................................................................................................#

#Three types of profiles

def profile1_view(request):
    if request.user.id != None:
        q = Profile.objects.get(user=request.user)
        webmail = q.webmail
        return render(request,'portal/profile1.html',{'user':request.user , 'webmail': webmail})
    else:
        return HttpResponseRedirect('/portal/login_page/')


def profile2_view(request):
    if request.user.id != None:
        q=Profile.objects.get(user=request.user)
        webmail=q.webmail
        return render(request, 'portal/profile2.html',{'user':request.user , 'webmail': webmail})
    else:
        return HttpResponseRedirect('/portal/login_page/')


def profile3_view(request):
    if request.user.id != None:
        q = Profile.objects.get(user=request.user)
        webmail = q.webmail
        return render(request, 'portal/profile3.html',{'user':request.user , 'webmail': webmail})
    else:
        return HttpResponseRedirect('/portal/login_page/')



#......................................................................................................................#


#view for logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/portal/login_page/')


#......................................................................................................................#

#view to create a team by user 2


def get_team(name,year):
    try:
        return team_detail.objects.get(team_name =name,year=year)
    except ObjectDoesNotExist:
        return None




def create_team_page(request):
    if request.user.is_authenticated():
        return render(request,'portal/create.html')
    else:
        return HttpResponseRedirect('/portal/login_page/')


def create_team(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            name = request.POST['team']
            subtitle = request.POST['subtitle']
            year = request.POST['year']
            under = request.POST['uta']
            team_name = get_team(name,year)
            q = Profile.objects.get(user=request.user)
            webmail = q.webmail
            x = type2.objects.filter(webmail = webmail).values_list('position',flat=True)
            if not x.exists():
                x = type1.objects.filter(webmail = webmail).values_list('position',flat=True)
            created_by = x[0]
            # if team_name is None:
            #     obj = models.team(name=name)
            #     obj.save()
            #     team_name= get_team(name)
            u1 = request.POST['bodies']
            u2 = request.POST['hostels']
            if team_name is not None:
                    return HttpResponse("Team already exists")
            if under == "dept_body":
                under = u1
            if under == "hostel_team":
                under = "Hostel: " + u2

            obj1 = models.team_detail(team_name = name,subtitle = subtitle, year = year , under = under , created_by = created_by)
            obj1.name = team_name
            obj1.creator_name = request.user
            obj1.save()
            qu = path.objects.get(under = under)
            obj2 = models.team_approval_progress(team_created_by = created_by,under = under,  pending_at = qu.stage1 , team_year = year , request_at_stage =1, team_creater_name = request.user)
            obj2.request_team = obj1
            obj2.save()

            return HttpResponseRedirect('/portal/login_page/')
        else:
            return HttpResponseRedirect('/portal/create_team_page/')
    else:
        return HttpResponseRedirect('/portal/login_page/')

#......................................................................................................................#




def search_team(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            search_text = request.POST['search_text']
            if search_text == "":
                return HttpResponse("")
            team = team_detail.objects.filter(team_name__startswith=search_text)
        else:
            search_text = ''

        return render(request,'portal/ajax_search.html',{'team':team})
    else:
        return HttpResponseRedirect('/portal/login_page/')





def search_event_page(request):
    if request.user.is_authenticated():
        return render(request,'portal/search.html')

    else:
        return HttpResponseRedirect('/portal/login_page/')




def get_post(user , board ,team , post ,year):
    try:
        return request_progress.objects.get(request_user = user , board = board , request_post = post , request_event = team , request_year = year  )
    except ObjectDoesNotExist:
        return None


#......................................................................................................................#
#view to apply for an event by user 2, 3





def apply_event_page(request,team_id):
    if request.user.is_authenticated():
        q = team_detail.objects.get(id=team_id)
        return render(request,'portal/post_apply.html',{'team_id' : team_id , 'team' : q})
    else:
        return HttpResponseRedirect('/portal/login_page/')



def apply_event(request,team_id):
    if request.user.is_authenticated():
        # if request.method == 'POST':
            # event_name = request.POST['event_name']
            # year = request.POST['year']
            post = request.POST['post']
            try:
                q =  team_detail.objects.get(id = team_id)
            except: q = None
            if q is None:
                return HttpResponse("Team name or year is wrong")
            created_by = q.created_by
            board = q.under
            team_creater = q.creator_name
            # obj = models.request(team=event_name, year=year, post=post, send_by=request.user, created_by = created_by, board= board)
            # obj.save()
            obj = get_post(request.user , board , q.team_name, post ,q.year)
            if obj is None:
                obj1 = models.request_progress(request_at_stage = 0,request_user = request.user , board=board , pending_at = created_by,request_post= post, request_event = q.team_name, request_created_by = created_by,request_year = q.year, request_event_subtitle = q.subtitle, request_creater_name = team_creater)
                obj1.save()
                return HttpResponseRedirect('/portal/login_page/')
            else:
                return HttpResponse('already applied for this post')
    else:
        return HttpResponseRedirect('/portal/login_page/')


#......................................................................................................................#

#view to show request for approval

def show_request_user2(request):
    if request.user.is_authenticated():
        q = Profile.objects.get(user=request.user)
        webmail = q.webmail
        x = type2.objects.filter(webmail=webmail).values_list('position', flat=True)
        if not x.exists():
            x = type1.objects.filter(webmail=webmail).values_list('position', flat=True)
        user_position = x[0]
        a = request_progress.objects.filter(pending_at=user_position)       # pending request for post
        b = team_approval_progress.objects.filter(pending_at = user_position)     # pending request for teams
        return render(request,'portal/posts.html',{'posts_pending' : a, 'teams_pending' : b})
    else:
        return HttpResponseRedirect('/portal/login_page/')








def approval_request_user(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            # option = request.POST.getlist('option')
            request_id = request.POST['request_id']

            if 'submit' in request.POST:
                option = "approved"
            else:
                option = "rejected"

            request_user = request_progress.objects.get(id=request_id)
            q = record_progress.objects.get(request_name__request_event = request_user.request_event,request_name__request_post = request_user.request_post,request_name__request_user = request_user.request_user )
            a = request_user.request_at_stage + 1
            stage = "stage" + str(a)
            qstage = "stage" + str(request_user.request_at_stage)

            if option == "approved":
                obj2 = path.objects.values(stage).filter(under = request_user.board).values_list(stage , flat = True)
                setattr(q, qstage, "Approved by " + request_user.pending_at)
                q.save()
                to_be_approve_at = obj2[0]
                request_user.pending_at = to_be_approve_at
                request_user.request_at_stage = a
                if to_be_approve_at != 'none':
                    request_user.save()
                else:
                    request_user.pending = False
                    request_user.approved = True
                    request_user.save()
            if option == "rejected":
                setattr(q, qstage, "Rejected by " + request_user.pending_at)
                q.save()
                reason = request.POST['reason']
                request_user.rejection_reason = reason
                request_user.pending = False
                request_user.rejected = True
                request_user.rejected_by = request_user.pending_at
                request_user.pending_at = "none"
                request_user.save()
            return HttpResponseRedirect('/portal/pending/')
        else:
            return  HttpResponse("Error")
    else:
        return HttpResponseRedirect('/portal/login_page/')




def approval_team_request(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            # option = request.POST.getlist('option')
            request_id = request.POST['request_id']
            if 'submit' in request.POST:
                option = "approved"
            else:
                option = "rejected"

            request_user = team_approval_progress.objects.get(id=request_id)
            # return render(request,'portal/test.html',{'x':request_user})
            q = record_team_progress.objects.get(request_name__request_team__team_name = request_user.request_team.team_name , request_name__team_year = request_user.team_year)
            if q is None:
                return HttpResponse("team does not exists")
            # return render(request, 'portal/test.html', {'x': q})
            a = request_user.request_at_stage + 1
            stage = "stage" + str(a)
            qstage = "stage" + str(request_user.request_at_stage)
            if option == "approved":
                obj2 = path.objects.values(stage).filter(under=request_user.under).values_list(stage, flat=True)
                setattr(q, qstage, "Approved by " + request_user.pending_at)
                q.save()
                to_be_approve_at = obj2[0]
                request_user.pending_at = to_be_approve_at
                request_user.request_at_stage = a
                if to_be_approve_at != 'none':
                    request_user.save()
                else:
                    request_user.pending = False
                    request_user.approved = True
                    request_user.save()
            if option == "rejected":
                reason = request.POST['reason']
                setattr(q, qstage, "Rejected by " + request_user.pending_at)
                q.save()
                request_user.rejection_reason = reason
                request_user.pending = False
                request_user.rejected = True
                request_user.rejected_by = request_user.pending_at
                request_user.pending_at = "none"
                request_user.save()
            return HttpResponseRedirect('/portal/pending/')
        else:
            return HttpResponse("Error")
    else:
        return HttpResponseRedirect('/portal/login_page/')







def show_pending_request(request):
    if request.user.is_authenticated():
        obj = request_progress.objects.filter(request_user = request.user)
        q = Profile.objects.get(user=request.user)
        webmail = q.webmail
        x = type2.objects.filter(webmail=webmail).values_list('position', flat=True)
        if not x.exists():
            x = type1.objects.filter(webmail=webmail).values_list('position', flat=True)
        else:
            user_position = x[0]
        if not x.exists():
            user_position = ""
        else:
            user_position = x[0]

        obj2 = team_approval_progress.objects.filter(team_created_by = user_position)
        obj3 = request_progress.objects.filter(pending_at=user_position)  # pending request for post
        obj4 = team_approval_progress.objects.filter(pending_at=user_position)
        return render(request,'portal/index.html',{'obj':obj , 'obj2': obj2, 'user3':user_position ,'obj3':obj3, 'obj4':obj4 })
    else:
        return  HttpResponseRedirect('/portal/login_page/')




def test(request):
    return render(request,'portal/index.html')
