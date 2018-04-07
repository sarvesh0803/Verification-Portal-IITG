# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,AnonymousUser
from django.shortcuts import HttpResponseRedirect,HttpResponse
from .models import Profile,type1,type2,team_detail,request_progress,path,record_progress,team_approval_progress,record_team_progress
from django.core.exceptions import ObjectDoesNotExist
from . import models
from io import BytesIO
from django import utils
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.conf import settings
from django.template import RequestContext
from django.http import  JsonResponse
import poplib
from django.views.generic import View
import os
from weasyprint import HTML,CSS
from django.template.loader import get_template
from django.template import RequestContext
from io import StringIO,BytesIO
from wkhtmltopdf.views import PDFTemplateResponse
from reportlab.pdfgen import canvas
from . import constants
# Create your views here.




#......................................................................................................................#
#view for login from webmail

def check_status(request):
    try:
        obj = Profile.objects.get(user=request.user)
    except:
        obj = None
    return obj


def get_user(webmail):
    try:
        return Profile.objects.get(webmail=webmail)
    except ObjectDoesNotExist:
        return None


def login_page(request):
    if request.user.is_authenticated:

        obj = check_status(request)
        if obj is not None:
            if obj.first_time_login == True:
                return HttpResponseRedirect('/portal/edit_profile_page/')
            else:
                return HttpResponseRedirect('/portal/pending/')
        else:
            return HttpResponseRedirect('/portal/error/')

    else:
        return render(request,'portal/login.html')
#

# def login_view(request):
#     if request.POST:
#         webmail = request.POST['webmail']
#         password = request.POST['password']
#         server = request.POST['server']
#         i = 0
#         try:
#             response = poplib.POP3_SSL(host=server, port=995)
#             response.user(webmail)
#             password_string = response.pass_(pswd=password)
#             if b'OK' in password_string:
#                 response.quit()
#                 # return HttpResponse("sdf")
#                 # username = get_user(webmail)
#                 try :
#                     username = User.objects.get(username = webmail )
#                 except:
#                     username = None
#                 if username is not None:
#                     username.set_password(password)
#                     username.save()
#                     user = authenticate(username = username , password = password)
#                     login(request, user)
#                     if user is not None:
#                         if    user.profile.first_time_login == True:
#                             return HttpResponseRedirect('/portal/edit_profile_page/')
#                 else:
#                     email = webmail + "@iitg.ernet.in"
#                     new_user = User.objects.create_user(username = webmail, password=password,email=email)
#                     new_user.save()
#                     user = Profile.objects.get(user =  new_user.id)
#                     user.webmail = webmail
#                     user.save()
#                     log_user = authenticate(username=webmail, password=password)
#                     login(request, log_user)
#                 return HttpResponseRedirect('/portal/pending/')
#             # else:
#             #     return HttpResponse( 'webmail or password is wrong')
#         except poplib.error_proto:
#             i= 1
#             return render(request,'portal/login.html', {'i':i})
#     else:
#         return HttpResponseRedirect('/portal/login_page/')
#     return HttpResponseRedirect('/portal/login_page/')






def login_view(request):
    if request.POST:
        webmail = request.POST['webmail']
        password = request.POST['password']
        username = get_user(webmail)

        if username is not None:
            user = authenticate(username = username , password= password)
            login(request, user)
            if webmail in constants.qu:
                user.profile.first_time_login = False
                user.profile.save()
            if user is not None:

                if user.profile.first_time_login == True:
                    return HttpResponseRedirect('/portal/edit_profile_page/')
                #    else:
                # return HttpResponseRedirect('/portal/pending/')
            # else:
            #    HttpResponse("user doesnt exist")
        else:

            return HttpResponseRedirect('/portal/error/')
        # else:
        #     raise poplib.error_proto("-ERR Authentication failed.")
    else:
        return HttpResponseRedirect('/portal/login_page/')
    return HttpResponseRedirect('/portal/login_page/')

#...................    ...................................................................................................#


#view for logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/portal/login_page/')


#......................................................................................................................#

#view to create a team by user 2


def get_team(name,year,under):
    try:
        return team_detail.objects.get(team_name =name,year=year,under = under)
    except ObjectDoesNotExist:
        return None




def create_team_page(request):
    if request.user.is_authenticated:
        obj = check_status(request)
        if obj is not None:
            if obj.first_time_login == True:
                return HttpResponseRedirect('/portal/edit_profile_page/')
            else:
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
                if user_position == "":
                    return HttpResponseRedirect('/portal/error/')
                else:
                    return render(request,'portal/create.html' , { 'web' : constants.qu , 'webmail' : webmail })
        else:
            return HttpResponseRedirect('/portal/error/')
    else:
        return HttpResponseRedirect('/portal/login_page/')


def create_team(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['team']
            subtitle = request.POST['subtitle']
            year = request.POST['year']
            under = request.POST['uta']
            team_name = get_team(name,year,under)
            q = Profile.objects.get(user=request.user)
            webmail = q.webmail
            x = type2.objects.filter(webmail = webmail).values_list('position',flat=True)
            if not x.exists():
                x = type1.objects.filter(webmail = webmail).values_list('position',flat=True)
            created_by = x[0]

            chairman = { 'Cultural Board': 'chrcult', 'Welfare Board' : 'chrwb' , 'Hostel Affairs Board' :'chr_hab', 'Sports Board' : 'chrsports','Technical Board': 'chrtech', 'Student Alumni Interaction Linkage' :'doaaer' , 'Student Academic Board' : 'doaa' ,'Campus Broadcasting System' : 'dos' , 'Student Web Committee': 'dos' , 'Others' : 'dos' }
            y = chairman.get(under)

            u1 = request.POST['bodies']
            u2 = request.POST['hostels']
            if team_name is not None:
                    return HttpResponse("Team already exists")
            z = under
            if under == "dept_body":
                under = u1

            if under == "Cultural Board":
                logo = "cult"
                color = "blue grey"
            elif under == "Technical Board":
                logo = "tech"
                color = "amber"
            elif under == "Welfare Board":
                logo = "welf"
                color = "teal"
            elif under == "Sports Board":
                logo = "sports"
                color = "grey"
            elif under == "Campus Broadcasting System":
                logo = "cbs"
                color = "green"
            elif under == "Students' Academic Board":
                logo = "sab"
                color = "red"
            elif under == "Student Alumni Interaction Linkage":
                logo = "sail"
                color = "orange"
            elif under == "Students' Web Committee":
                logo = "swc"
                color = "purple"
            elif under == "ACE":
                logo = "ace"
                color = "indigo"
            elif under == "Cepstrum":
                logo = "cepstrum"
                color = "pink"
            elif under == "CSEA":
                logo = "csea"
                color = "light green"
            elif under == "Matrix":
                logo = "matrix"
                color = "light blue"
            elif under == "MESA":
                logo = "mesa"
                color = "cyan"
            elif under == "Reflux":
                logo = "reflux"
                color = "yellow"
            elif under =="hostel_team":
                logo = "hostel"
                color = "lime"
            elif under == "Others":
                logo = "others"
                color = "brown"
            elif under == "Centre for Career Development":
                logo = "ccd"
                color = "blue"
            elif under =="Hostel Affairs Board":
                logo = "hab"
                color = "deep purple"


            if under == "hostel_team":
                under = "Hostel: " + u2
            faculty = {'CSEA': '', 'Cepstrum': 'deb.sikdar', 'Matrix': '', 'ACE': 'rbharti', 'MESA': 'spal',
                       'Reflux': 'psgp'}
            w = faculty.get(under)
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

            qu = path.objects.get(under=under)

            if webmail == "vp":
                if z == "dept_body" or z == "hostel_team" :
                    obj1 = models.team_detail(team_name=name, subtitle=subtitle, year=year, under=under,
                                              created_by=created_by)
                    obj1.name = team_name
                    obj1.creator_name = request.user.profile.username
                    obj1.save()
                    obj2 = models.team_approval_progress(team_created_by=created_by, under=under, pending_at=qu.stage1,
                                                         team_year=year, request_at_stage=1,
                                                         team_creater_name=request.user, logo=logo, color=color)
                    obj2.request_team = obj1
                    obj2.save()
                else:
                    obj1 = models.team_detail(team_name=name, subtitle=subtitle, year=year, under=under,
                                              created_by=created_by)
                    obj1.name = team_name
                    obj1.creator_name = request.user.profile.username
                    obj1.save()
                    obj2 = models.team_approval_progress(team_created_by=created_by, under=under, pending_at="none",
                                                         team_year=year, request_at_stage=1,
                                                         team_creater_name=request.user, logo=logo, color=color)
                    obj2.request_team = obj1
                    obj2.approved = True
                    obj2.pending = False
                    obj2.save()

            elif webmail == y or webmail == "dos" or webmail == w:

                obj1 = models.team_detail(team_name=name, subtitle=subtitle, year=year, under=under,
                                          created_by=created_by)
                obj1.name = team_name
                obj1.creator_name = request.user.profile.username
                obj1.save()
                obj2 = models.team_approval_progress(team_created_by=created_by, under=under, pending_at="none",
                                                     team_year=year, request_at_stage=1,
                                                     team_creater_name=request.user, logo=logo, color=color)
                obj2.request_team = obj1
                obj2.approved = True
                obj2.pending = False
                obj2.save()


            else:

                obj1 = models.team_detail(team_name = name,subtitle = subtitle, year = year , under = under , created_by = created_by)
                obj1.name = team_name
                obj1.creator_name = request.user.profile.username
                obj1.save()
                if qu.stage1 == user_position:
                    obj2 = models.team_approval_progress(team_created_by = created_by,under = under,  pending_at = qu.stage2 , team_year = year , request_at_stage =2, team_creater_name = request.user, logo = logo , color = color)
                    obj2.request_team = obj1
                    obj2.save()
                elif qu.stage2 == user_position:
                    obj2 = models.team_approval_progress(team_created_by=created_by, under=under, pending_at=qu.stage3,
                                                         team_year=year, request_at_stage=3, team_creater_name=request.user,
                                                         logo=logo, color=color)
                    obj2.request_team = obj1
                    obj2.save()
                else:
                    obj2 = models.team_approval_progress(team_created_by=created_by, under=under, pending_at=qu.stage1,
                                                         team_year=year, request_at_stage=1, team_creater_name=request.user,
                                                         logo=logo, color=color)
                    obj2.request_team = obj1
                    obj2.save()
            return HttpResponseRedirect('/portal/login_page/')
        else:
            return HttpResponseRedirect('/portal/create_team_page/')
    else:
        return HttpResponseRedirect('/portal/login_page/')

#......................................................................................................................#




def search_team(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            search_text = request.POST['search_text']
            filter_name1 = request.POST['filter1']
            filter_name2 = request.POST['filter2']
            bodies = request.POST['bodies']
            hostels = request.POST['hostels']
            if filter_name2 == "dept_body":
                filter_name2 = bodies
            if filter_name2 == "hostel_team":
                filter_name2 = hostels

            if search_text == "":
                return HttpResponse("")
            if filter_name1 == "All" and filter_name2 == "All":
                team = team_detail.objects.filter(team_name__startswith=search_text)
                profile = User.objects.filter(username__startswith = search_text )
            if filter_name1 == "All" and filter_name2 != "All":
                team = team_detail.objects.filter(team_name__startswith=search_text , under = filter_name2)

                profile = User.objects.filter(username__startswith=search_text)
            if filter_name1 =='Team' and filter_name2 == "All":
                team = team_detail.objects.filter(team_name__startswith=search_text)
                profile = []
            if filter_name1 =='Team' and filter_name2 != "All":
                team = team_detail.objects.filter(team_name__startswith=search_text , under = filter_name2)
                profile = []
            if filter_name1 == 'Profile':
                profile = User.objects.filter(username__startswith=search_text)
                team = []
            q = Profile.objects.get(user=request.user)
            webmail = q.webmail
            x = type1.objects.filter(webmail=webmail).values_list('position', flat=True)
            if not x.exists():
                user_position = []
            else:
                user_position = x[0]


        else:
            search_text = ''
            return HttpResponseRedirect('/portal/error/')

        return render(request,'portal/ajax_search.html',{'team':team , 'profile' : profile, 'type1' : user_position, 'type': constants.view})
    else:
        return HttpResponseRedirect('/portal/login_page/')





def search_event_page(request):
    if request.user.is_authenticated:
        obj = check_status(request)
        if obj is not None:
            if obj.first_time_login == True:
                return HttpResponseRedirect('/portal/edit_profile_page/')
            else:
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
                return render(request,'portal/search.html', { 'user3' : user_position , 'web' : constants.qu , 'webmail' : webmail})
        else:
            return HttpResponseRedirect('/portal/error/')

    else:
        return HttpResponseRedirect('/portal/login_page/')





def get_post(user , board ,team , post ,year):
    try:
        return request_progress.objects.get(request_user = user.profile.username , board = board , request_post = post , request_event = team , request_year = year)
    except ObjectDoesNotExist:
        return None


#......................................................................................................................#
#view to apply for an event by user 2, 3




#
# def apply_event_page(request,team_id):
#     if request.user.is_authenticated:
#         q = team_detail.objects.get(id=team_id)
#         return render(request,'portal/post_apply.html',{'team_id' : team_id , 'team' : q})
#     else:
#         return HttpResponseRedirect('/portal/login_page/')
#


def apply_event(request,team_id):
    if request.user.is_authenticated:
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
            p = Profile.objects.get(user=request.user)
            webmail = p.webmail
            y = type2.objects.filter(webmail=webmail).values_list('position', flat=True)
            if not y.exists():
                y = type1.objects.filter(webmail=webmail).values_list('position', flat=True)
            else:
                user_position = y[0]
            if not y.exists():
                user_position = ""
            else:
                user_position = y[0]


            x = team_approval_progress.objects.get(request_team  = q)
                # obj = models.request(team=event_name, year=year, post=post, send_by=request.user, created_by = created_by, board= board)
            # obj.save()

            obj = get_post(request.user , board , q.team_name, post ,q.year)
            if obj is None:
                if user_position == created_by:
                    obj2 = path.objects.values("stage1").filter(under=board).values_list("stage1", flat=True)
                    if user_position == obj2[0]:
                        obj1 = models.request_progress(request_at_stage=0, request_user=request.user.profile.username, board=board,
                                                       pending_at='none', request_post=post,
                                                       request_event=q.team_name,
                                                       request_created_by=created_by, request_year=q.year,
                                                       request_event_subtitle=q.subtitle,
                                                       request_creater_name=team_creater,
                                                       event_logo=x.logo, event_color=x.color,request_user_webmail = webmail)
                        obj1.approved = True
                        obj1.pending = False
                        obj1.save()
                    else:
                        obj1 = models.request_progress(request_at_stage=1, request_user=request.user.profile.username, board=board,
                                                       pending_at=obj2[0], request_post=post,
                                                       request_event=q.team_name,
                                                       request_created_by=created_by, request_year=q.year,
                                                       request_event_subtitle=q.subtitle,
                                                       request_creater_name=team_creater,
                                                       event_logo=x.logo, event_color=x.color, request_user_webmail = webmail)
                        obj1.save()
                else:
                    obj1 = models.request_progress(request_at_stage = 0,request_user = request.user.profile.username , request_user_webmail = webmail, board=board , pending_at = created_by,request_post= post, request_event = q.team_name, request_created_by = created_by,request_year = q.year, request_event_subtitle = q.subtitle, request_creater_name = team_creater, event_logo = x.logo, event_color = x.color)
                    obj1.save()
                return HttpResponseRedirect('/portal/pending/')
            elif obj.rejected == True:
                obj.delete()



                obj1 = models.request_progress(request_at_stage=0, request_user=request.user.profile.username, board=board,
                                               pending_at=created_by, request_post=post, request_event=q.team_name,
                                               request_created_by=created_by, request_year=q.year,
                                               request_event_subtitle=q.subtitle, request_creater_name=team_creater,
                                               event_logo=x.logo, event_color=x.color,request_user_webmail = webmail )

                obj1.save()
                return HttpResponseRedirect('/portal/pending/')
            else:
                return HttpResponse('already applied for this post')
    else:
        return HttpResponseRedirect('/portal/login_page/')


#......................................................................................................................#



def approval_request_user(request):
    if request.user.is_authenticated:
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
            a = a + 1
            stage_next =  "stage" + str(a)
            qstage_next = "stage" + str(a+1)


            if option == "approved":
                if request_user.request_created_by == "Vice President" or request_user.request_created_by in constants.faculty or request_user.request_created_by in constants.chairman :
                    setattr(q, qstage, "Approved by " + request_user.pending_at)
                    q.save()
                    request_user.pending_at = "none"
                    request_user.request_at_stage = 1
                    request_user.pending = False
                    request_user.approved = True
                    request_user.save()
                else:
                    obj2 = path.objects.values(stage).filter(under = request_user.board).values_list(stage , flat = True)
                    obj3 = path.objects.values(stage_next).filter(under = request_user.board).values_list(stage_next , flat = True)
                    setattr(q, qstage, "Approved by " + request_user.pending_at)
                    q.save()
                    to_be_approve_at = obj2[0]
                    request_user.pending_at = to_be_approve_at
                    request_user.request_at_stage = a-1
                    to_be_approve_at_next = obj3[0]
                    if to_be_approve_at_next != 'none':
                        request_user.save()
                    else:
                        request_user.pending_at = "none"
                        request_user.pending = False
                        request_user.approved = True
                        request_user.save()
                    if to_be_approve_at == request_user.request_user:    #always matches at stage 1 so directly approve
                        request_user.pending_at = "none"
                        request_user.request_at_stage = 1
                        request_user.save()
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
            return HttpResponseRedirect('/portal/error/')
    else:
        return HttpResponseRedirect('/portal/login_page/')




def approval_team_request(request):
    if request.user.is_authenticated:
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
            return HttpResponseRedirect('/portal/error/')
    else:
        return HttpResponseRedirect('/portal/login_page/')







def show_pending_request(request):
    if request.user.is_authenticated:
        obj = check_status(request)
        if obj is not None:

            if obj.first_time_login == True:
                return HttpResponseRedirect('/portal/edit_profile_page/')
            else:
                obj = request_progress.objects.filter(request_user_webmail = request.user.profile.webmail)
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
                request_len = len(obj4) + len(obj3)
                return render(request,'portal/index.html',{'obj':obj , 'obj2': obj2, 'user3':user_position ,'obj3':obj3, 'obj4':obj4 ,'request_len' : request_len , 'web' : constants.qu , 'webmail' : webmail})
        else:
            return HttpResponseRedirect('/portal/error/')
    else:
        return  HttpResponseRedirect('/portal/login_page/')




def help(request):
    if request.user.is_authenticated:
        obj = check_status(request)
        if obj is not None:
            if obj.first_time_login == True:
                return HttpResponseRedirect('/portal/edit_profile_page/')
            else:
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
                return render(request,'portal/help.html',{'user3': user_position , 'web' : constants.qu , 'webmail' : webmail })
        else:
            return HttpResponseRedirect('/portal/error/')
    else:
        return  HttpResponseRedirect('/portal/login_page/')



def profile(request):
    if request.user.is_authenticated:
        obj = check_status(request)
        if obj is not None:
            if obj.first_time_login == True:
                return HttpResponseRedirect('/portal/edit_profile_page/')
            else:
                obj = request_progress.objects.filter(request_user_webmail=request.user.profile.webmail, approved = True)
                q = Profile.objects.get(user=request.user)
                webmail = q.webmail
                if webmail in constants.qu:
                    return HttpResponseRedirect("/portal/error/")
                x = type2.objects.filter(webmail=webmail).values_list('position', flat=True)
                if not x.exists():
                    x = type1.objects.filter(webmail=webmail).values_list('position', flat=True)
                else:
                    user_position = x[0]
                if not x.exists():
                    user_position = ""
                else:
                    user_position = x[0]

                return render(request,'portal/profile.html' ,{'user3': user_position , 'post': obj})
        else:
            return HttpResponseRedirect('/portal/error/')
    else:
        return  HttpResponseRedirect('/portal/login_page/')



def view_profile(request,roll_no,id):
    if request.user.is_authenticated:
        try:
            profile = User.objects.get(id = id)
        except: profile = None
        try:
            qu = Profile.objects.get(roll_no=roll_no)
        except:
            qu = None
        if qu is None:
            return HttpResponseRedirect('/portal/error/')
        if profile is None:
            return HttpResponse("No such user")
        else:
            obj = request_progress.objects.filter(request_user_webmail = profile.profile.webmail , approved=True)
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
            i = 0
            return render(request, 'portal/search_profile.html', {'user3': user_position, 'profile': profile, 'post': obj, 'i': i })
    else:
        return  HttpResponseRedirect('/portal/login_page/')



def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            obj = Profile.objects.get(user=request.user)
            name = request.POST['name']
            roll_no = request.POST['roll_no']
            if roll_no == "":
                roll_no = obj.roll_no
            if name == "":
                name = obj.user.username
            obj.roll_no = roll_no
            obj.first_time_login = False
            obj.username = name
            obj.save()
            return HttpResponseRedirect('/portal/pending/')

        else:
            return HttpResponseRedirect('/portal/error/')
    else:
        return HttpResponseRedirect('/portal/login_page/')



def edit_profile_page(request):
    if request.user.is_authenticated:
        obj = Profile.objects.get(user = request.user)
        if obj.first_time_login == True:
            return render(request, 'portal/first_time_login.html')
        else:
            return HttpResponseRedirect('/portal/login_page/')
    else:
        return HttpResponseRedirect('/portal/login_page/')

def custom_404(request):
    return render(request,'portal/404.html')



def custom_500(request):
    return render(request, 'portal/500.html')


def error(request):
    return render(request,'portal/404.html')




def fetch_resources(uri, rel):
    path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))

    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result,link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='.pdf')
    return None



def test(request):
    obj = request_progress.objects.filter(request_user=request.user.profile.username, approved=True)
    return render(request,'portal/feedback.html' , { 'post': obj })


class GeneratePDF(View):
    template = 'portal/template.html'  # the template
    header_template = 'portal/header.html'
    footer_template = 'portal/footer.html'

    def get(self, request):
        if request.user.is_authenticated:
            roll =request.user.profile.roll_no
            file = str(roll) + ".pdf"
            obj = request_progress.objects.filter(request_user=request.user.profile.username, approved=True)
            data = { 'post': obj }  # data that has to be renderd to pdf templete
            # render(request,'portal/template.html',{ 'post': obj })
            response = PDFTemplateResponse(request=request,
                                           template=self.template,
                                           filename=file,
                                           context=data,
                                           show_content_in_browser=False,
                                           header_template='portal/header.html',
                                           footer_template=self.footer_template,
                                           cmd_options={'margin-top': 60,
                                                        "zoom": 1,
                                                        'margin-bottom': 25,
                                                        "viewport-size": "1366 x 513",
                                                        'javascript-delay': 1000,
                                                        "no-stop-slow-scripts": True},
                                           )
            return response


def feedback(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            text = request.POST['feedback_text']
            pic = request.FILES.get('pic', 'feedback/none.png')
            feedback = models.feedback(user = request.user , feedback_text = text, image=pic)
            feedback.save()
            return HttpResponseRedirect('/portal/help/')
        else:
            return HttpResponseRedirect('/portal/error/')