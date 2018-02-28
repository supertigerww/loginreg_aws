# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import user,item
import bcrypt
import json

# Create your views here.
def index(request):
    return render(request, 'loginregapp/index.html')
def register(request):
    if request.method == 'POST':
        errors =  user.objects.validation(request.POST)
        if 'user' in errors:
            request.session['currentuser']=errors['user']
            
            return redirect('/dashboard')
        else:
            for register,error in errors.iteritems():
                messages.error(request, error, extra_tags=register)
            return redirect('/main')
    else:
        return redirect('/main')
def login(request):
    loginerrors = user.objects.loginvalidation(request.POST)
    if len(loginerrors):
        for login, error in loginerrors.iteritems():
            messages.error(request,error,extra_tags=login)
            return redirect('/main')
    else:
        currentuser=user.objects.get(username=request.POST['username'])
        request.session['currentuser']=currentuser
        return redirect('/dashboard')
def success(request):
    if "currentuser"  in request.session:
        showuser = request.session['currentuser']
        context={
            "currentuser":showuser,
            "youritems":showuser.wished_items.all(),

            "otheritems":item.objects.exclude(users=showuser)
            }
        return render(request, 'loginregapp/success.html',context)
    else:
        return redirect('/main')
def logout(request):
    request.session.clear()
    return redirect('/main')
def createprocess(request):
    if request.method == "POST":
        itemerrors = item.objects.itemvalidation(request.POST)
        if len(itemerrors):
            for newitem , error in itemerrors.iteritems():
                messages.error(request, error, extra_tags=newitem)
            return redirect('/wish_items/create')
        else:
            newitem=item.objects.create(name=request.POST['name'],added_by=request.session['currentuser'])
            newitem.users.add(request.session['currentuser'])
            return redirect('/dashboard')
    else:
        return redirect('/wish_items/create')
def additem(request):
    return render(request, 'loginregapp/create.html')
def showitem(request,id):
    iteminfo={
        "wished_users":user.objects.raw("SELECT * FROM loginregapp_user JOIN loginregapp_item_users ON loginregapp_user.id=loginregapp_item_users.user_id JOIN loginregapp_item ON loginregapp_item.id=loginregapp_item_users.item_id WHERE loginregapp_item.id=%s",[id])
    }
    return render(request, 'loginregapp/show.html',iteminfo)
def addwishlistprocess(request,id):
    this_item=item.objects.get(id=id)
    this_user=user.objects.get(name=request.session['currentuser'].name)
    this_item.users.add(this_user)
    return redirect('/dashboard')
def removewishlist(request,id):
    this_item=item.objects.get(id=id)
    this_user=user.objects.get(name=request.session['currentuser'].name)
    this_item.users.remove(this_user)
    return redirect('/dashboard')
def delete(request,id):
    this_item=item.objects.get(id=id)
    this_item.delete()
    return redirect('/dashboard')

    
    
    
        


    

               
               
               


