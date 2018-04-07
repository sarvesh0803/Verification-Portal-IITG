# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import type1,type2,Profile,team_detail,path,request_progress,record_progress,team_approval_progress,record_team_progress,feedback

# Register your models here.

admin.site.register(type1)
admin.site.register(type2)
admin.site.register(Profile)
admin.site.register(team_detail)
admin.site.register(path)
admin.site.register(request_progress)
admin.site.register(record_progress)
admin.site.register(team_approval_progress)
admin.site.register(record_team_progress)
admin.site.register(feedback)
