# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
regex=re.compile(r'^[a-zA-Z0-9]+$')
import datetime

# Create your models here.
class usermanager(models.Manager):
    def validation(self,postData):
        errors = {}
        if len(postData['name']) <  3:
            errors['name'] = "Name should be no fewer than 3 characters"
        if any(char.isdigit() for char in postData['name']) == True:
            errors['name'] = "Name can not have numbers"
        if len(postData['username']) <  3:
            errors['username'] = "Username should be no fewer than 3 characters"
        if not regex.match(postData['password']):
            errors['password'] = "Password can not have special characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be greater than 8 characters"
        if postData['confirmpassword'] !=postData['password']:
            errors['confirmpassword'] = "Passwords do not match"
        if len(errors)==0:
            bcryptpassword = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            currentuser=user.objects.create(name=postData['name'],username=postData['username'],password=bcryptpassword)
            errors['user']=currentuser
        return errors



    def loginvalidation(self,postData):
        loginerrors={}
        if len(postData['username']) <  3:
            loginerrors['username'] = "Username should be no fewer than 3 characters"
        if not regex.match(postData['password']):
            loginerrors['password'] = "Password can not have special characters"
        if len(postData['password']) < 8:
            loginerrors['password'] = "Password must be greater than 8 characters"
        if user.objects.filter(username=postData['username']):
            currentuser=user.objects.filter(username=postData['username'])[0]
            hashed_pw=currentuser.password
            if bcrypt.checkpw(postData['password'].encode(), hashed_pw.encode()) == True:
                pass
            else:
                loginerrors['password']= "Wrong username or password"
        else:
            loginerrors['username']= "Wrong username or password"
        return loginerrors
    
class itemmanager(models.Manager):
    def itemvalidation(self,postData):
        itemerrors={}
        if len(postData['name']) == 0:
            itemerrors['name'] = "No empty entries"
        if postData['name'] < 3:
            itemerrors['name'] = "Item name should be more than 3 characters"
        return itemerrors


    

class user(models.Model):
    name =  models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    datehired = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = usermanager()

class item(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(user, related_name="wished_items")
    added_by = models.ForeignKey(user,related_name="added_item")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = itemmanager()

