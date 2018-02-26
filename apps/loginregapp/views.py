# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import user
import bcrypt
import json

# Create your views here.
def index(request):
    return render(request, 'loginregapp/index.html')
def register(request):
    if request.method == 'POST':
        errors =  user.objects.validation(request.POST)
        if 'user' in errors:
            request.session['currentuser_id']=errors['user'].id
            request.session['currentuser_name']=errors['user'].first_name
            
            return redirect('/success')
        else:
            for register,error in errors.iteritems():
                messages.error(request, error, extra_tags=register)
            return redirect('/')
    else:
        return redirect('/')
def login(request):
    loginerrors = user.objects.loginvalidation(request.POST)
    if len(loginerrors):
        for login, error in loginerrors.iteritems():
            messages.error(request,error,extra_tags=login)
            return redirect('/')
    else:
        currentuser=user.objects.get(email=request.POST['email'])
        request.session['currentuser_id']=currentuser.id
        request.session['currentuser_name']=currentuser.first_name
        return redirect('/success')
def success(request):
    if "currentuser_id"  in request.session:
        return render(request, 'loginregapp/success.html')
    else:
        return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')
    
        


    

               
               
               


