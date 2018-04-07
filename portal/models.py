# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User



#model for storing what are the positions type1 and type2 users are holding



class type1(models.Model):
    board = models.CharField(max_length=200,default="")
    position= models.CharField(max_length=200,default="")
    webmail = models.CharField(max_length=200,default="")

    def __str__(self):
        return self.position


class type2(models.Model):
    board = models.CharField(max_length=200,default="")
    position= models.CharField(max_length=200,default="")
    webmail = models.CharField(max_length=200,default="")

    def __str__(self):
        return self.position

# ....................................................................................................................#

#model for profile of user

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=200,default="")
    board = models.CharField(max_length=200,default="")
    webmail = models.CharField(max_length=200,default="")
    roll_no = models.IntegerField(default="0")
    first_time_login = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


#....................................................................................................................#

#model to create a team


class team_detail(models.Model):
    team_name = models.CharField(max_length=200,default="")
    subtitle = models.CharField(max_length=600, default="")
    year = models.CharField(max_length=300,default="")
    under = models.CharField(max_length=200,default="")
    created_by = models.CharField(max_length=200,default="")
    creator_name = models.CharField(max_length=200,default="")



    def __str__(self):
        return self.team_name


#......................................................................................................................#





class team_approval_progress(models.Model):
    request_team = models.ForeignKey(team_detail,on_delete=models.CASCADE,related_name="detail")
    team_creater_name = models.CharField(max_length=200,default="")
    team_created_by = models.CharField(max_length=200,default="")
    team_created_webmail = models.CharField(max_length=200,default="")
    team_year = models.CharField(max_length=200,default="")
    request_at_stage = models.IntegerField(default=0)
    under = models.CharField(max_length=200)
    pending_at = models.CharField(max_length=200)
    rejection_reason = models.CharField(max_length=400,default="")
    rejected_by = models.CharField(max_length=200, default="")
    color = models.CharField(max_length=100,default="")
    logo = models.CharField(max_length=100, default="")
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)

    def __str__(self):
        return self.team_created_by



#......................................................................................................................#




class record_team_progress(models.Model):
    request_name = models.ForeignKey(team_approval_progress,on_delete=models.CASCADE,related_name="team_approval_progress")
    stage0 = models.CharField(max_length=200,default="none")
    stage1 = models.CharField(max_length=200,default="none")
    stage2 = models.CharField(max_length=200,default="none")
    stage3 = models.CharField(max_length=200,default="none")


    def __str__(self):
        return  self.request_name.team_created_by



def create_record_team_progress(sender, **kwargs):
    if kwargs['created']:
        user_profile = record_team_progress.objects.create(request_name=kwargs['instance'])


post_save.connect(create_record_team_progress, sender=team_approval_progress)



#......................................................................................................................#




class request_progress(models.Model):
    request_created_by = models.CharField(max_length=200,default="")
    request_creater_name = models.CharField(max_length=200,default="")
    request_event = models.CharField(max_length=200,default="")
    event_logo = models.CharField(max_length=200,default="")
    event_color = models.CharField(max_length=200, default="")
    request_event_subtitle = models.CharField(max_length=200, default="")
    request_post = models.CharField(max_length=300)
    request_at_stage = models.IntegerField(default=0)
    request_user = models.CharField(max_length=200)
    request_user_webmail = models.CharField(max_length=200,default="")
    board = models.CharField(max_length=200)
    pending_at = models.CharField(max_length=200)
    request_year = models.CharField(max_length=200,default="")
    rejection_reason = models.CharField(max_length=400, default="")
    rejected_by = models.CharField(max_length=200,default="")
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)


    def __str__(self):
        return self.request_user




#......................................................................................................................#




class record_progress(models.Model):
    request_name = models.ForeignKey(request_progress,on_delete=models.CASCADE,related_name="request_progress")
    stage0 = models.CharField(max_length=200,default="none")
    stage1 = models.CharField(max_length=200,default="none")
    stage2 = models.CharField(max_length=200,default="none")
    stage3 = models.CharField(max_length=200,default="none")

    def __str__(self):
        return  self.request_name.request_user


    def multiply(value):
        return value*25;

def create_record_progress(sender, **kwargs):
    if kwargs['created']:
        user_profile = record_progress.objects.create(request_name=kwargs['instance'])


post_save.connect(create_record_progress, sender=request_progress)



#......................................................................................................................#


class path(models.Model):
    under = models.CharField(max_length=200,default="")
    stage1 = models.CharField(max_length=200, default="",null=True)
    stage2 = models.CharField(max_length=200, default="",null=True)
    stage3 = models.CharField(max_length=200, default="",null=True)
    stage4 = models.CharField(max_length=200, default="none")

    def __str__(self):
        return "under " + self.under



#......................................................................................................................#



class feedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    feedback_text = models.CharField(max_length=500, default="")
    image = models.ImageField(upload_to='feedback/',blank=True,default='media/feedback/none.png')



    def __str__(self):
        return self.user.username




