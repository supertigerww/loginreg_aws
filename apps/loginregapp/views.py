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
            request.session['currentuser_id']=errors['user'].id
            request.session['currentuser_name']=errors['user'].name
            
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
        request.session['currentuser_id']=currentuser.id
        request.session['currentuser_name']=currentuser.name
        return redirect('/dashboard')
def success(request):
    if "currentuser_id"  in request.session:
        context={
            "userid":request.session['currentuser_id'],
            "user_name":request.session['currentuser_name'],
            "youritems":item.objects.raw("SELECT * FROM loginregapp_item JOIN loginregapp_item_users ON loginregapp_item.id=loginregapp_item_users.item_id JOIN loginregapp_user ON loginregapp_user.id=loginregapp_item_users.user_id"),
            "otheritems":item.objects.raw("SELECT * FROM loginregapp_item JOIN loginregapp_item_users ON loginregapp_item.id=loginregapp_item_users.item_id JOIN loginregapp_user ON loginregapp_user.id=loginregapp_item_users.user_id"),
            
            

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
            newitem=item.objects.create(name=request.POST['name'])
            newitem.users.add(request.session['currentuser_id'])
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
    this_user=user.objects.get(name=request.session['currentuser_name'])
    this_item.users.add(this_user)
    return redirect('/dashboard')
def removewishlist(request,id):
    this_item=item.objects.get(id=id)
    this_user=user.objects.get(name=request.session['currentuser_name'])
    this_item.users.remove(this_user)
    return redirect('/dashboard')
def delete(request,id):
    this_item=item.objects.get(id=id)
    this_item.delete()
    return redirect('/dashboard')

    
    
    
        


    

               
               
               


