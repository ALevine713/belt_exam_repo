from __future__ import unicode_literals

from django.db import models
import re, datetime, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def reg(self, data):
        errors = []
        if len(data['name']) < 2:
            errors.append("Your name must be at least 2 characters long.")
        if not data['name'].isalpha():
            errors.append("First name may only be letters")
        if len(data['alias']) < 2:
            errors.append("Your Alias must be at least 2 characters long.")
        if not data['alias'].isalpha():
            errors.append("Last name may only be letters")
        if data['e_address'] == '':
            errors.append("Email may not be blank")
        if not EMAIL_REGEX.match(data['e_address']):
            errors.append("Please enter a vailid email address")
        try:
            User.objects.get(email = data['e_address'])
            errors.append("Email is already registered, please log in.")
        except:
            pass
        if len(data['pass_word']) < 8:
            errors.append("Password must be at least 8 characters long.")
        if data['pass_word'] != data['confirm_pass_word']:
            errors.append("Password and confirm password does not match.")
        if data['dob'] == '':
            errors.append("Birthdays are required")
        elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
            errors.append("Please enter a vaild birthday. Birthday can not be in the future!")
        if len(errors) == 0:
            print('no errors')
            data['pass_word'] = bcrypt.hashpw(data['pass_word'].encode('utf-8'), bcrypt.gensalt())
            new_user = User.objects.create(name=data['name'], alias=data['alias'], email=data['e_address'], password=data['pass_word'], birthday=data['dob'])
            return {
                'new': new_user,
                'error_list': None,
            }
        else:
            print(errors)
            return {
                'new': None,
                'error_list': errors
            }
    def log(self, log_data):
        errors = []
        try:
            found_user = User.objects.get(email=log_data['e_mail'])
            if bcrypt.hashpw(log_data['p_word'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
                errors.append("Incorrect Password.")
        except:
            errors.append("Email Address is not registered")
        if len(errors) == 0:
            return {
                'logged_user': found_user,
                'list_errors': None,
            }
        else:
            return {
                'logged_user': None,
                'list_errors': errors,
            }

class QuoteManager(models.Manager):
    def new(self, data):
        errors = []
        if len(data['author']) < 3:
            errors.append("can't authenticate a quote without knowing who said it. So... who said it??")
        if len(data['quote']) < 10:
            errors.append("wait.... what? that's not long enough to be a quote.")
        if len(errors) == 0:
            print('no errors')
            new_quote = Quote.objects.create(author=data['author'], quote=data['quote'], creator=data['creator'], favorite=data['favorite'])
            return {
                'new': new_quote,
                'error_list': None,
            }
        else:
            print(errors)
            return {
                'new': None,
                'error_list': errors
            }

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=100)
    quote = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="trip_creater")
    favorite = models.ForeignKey (User, related_name="favorited")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = QuoteManager()
