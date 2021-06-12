from django.db import models
import re

from django.db.models.base import Model

# Create your models here.


class UserManager(models.Manager):
    def validate(self, formData):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(formData["first_name"]) < 2:
            errors["first_name"] = "First Name should be at least 2 characters long"

        if len(formData["last_name"]) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters long"

        if len(formData["email"]) < 2:
            errors["email"] = "Email should be at least 2 characters long"
# test whether a field matches the pattern
        if not EMAIL_REGEX.match(formData['email']):
            errors['email'] = 'Invalid Email Address'

        email_check = self.filter(email=formData['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(formData["password"]) < 2:
            errors["password"] = "Password should be at least 2 characters long"

        if formData["confirm_password"] != formData["password"]:
            errors["confirm_password"] = "Passwords do not match"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    # user.liked_events
    # user.schedules


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    date_time = models.DateTimeField('01-02-2021')
    user_likes = models.ManyToManyField(User, related_name='liked_events')
    user = models.ForeignKey(
        User, related_name='schedules', on_delete=models.CASCADE)

    def __repr__(self):
        return f"<Event object: {self.title} {self.id}"
