from django.db import models
import re
from django.db.models.deletion import CASCADE

# Create your models here.
class UserManager(models.Manager):
    def sign_up_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['name']) < 2:
            errors["name"] = "Your name should be at least 2 characters"
        if len(postData['alias']) < 2:
            errors["username"] = "Your alias should be at least 2 characters"
        if len(postData["email"]) <= 1:
            errors["email"] = "Please try with a valid email"        
        if not EMAIL_REGEX.match(postData['email']):       
            errors["email"] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Your password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors["password"] = "Your password don't match with confirm, please write it again"
        return errors
    def sign_in_validator(self, postData):
        #errors = {}
        #EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #if not EMAIL_REGEX.match(postData['log_email']):       
        #    errors["log_email"] = "Invalid email address!"
        #user_pw = User.objects.get(password=postData["log_pw"])
        #if postData["log_pw"] != user_pw:
        #    errors["log_pw"] = "Your password don't match, please try again"
        #return errors
        pass

        

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255, default=True)
    user_hash = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Poke(models.Model):
    origin_user = models.ForeignKey(User, related_name='sent_pokes', on_delete=CASCADE, default=True)
    destination_user = models.ForeignKey(User, related_name='received_pokes', on_delete=CASCADE, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)