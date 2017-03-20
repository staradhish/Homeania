from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


"""
User table (id, first_name, last_name, email, password, joining_date, level_id) --->> auth_user default django table
Level table(level_id, level_name)
question table(question_id, question_content, level_id(FK))
answer table(answer_id, answer_content, question_id(FK), is_correct)
user_question_answer table( where we will save the last progress of user)
"""

class Level(models.Model):
    #myuser_id = models.ForeignKey(settings.AUTH_USER_MODEL)
    level_name = models.CharField(max_length=120)

    def __unicode__(self):
        return self.level_name


class Question(models.Model):
    question_content = models.TextField()
    level = models.ForeignKey(Level)

    def __unicode__(self):
        return self.question_content


class Answer(models.Model):
    answer_content = models.TextField()
    question = models.ForeignKey(Question, related_name="qus")
    is_correct = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.answer_content

# class result(models.Model):
#     user
#     level
#     qus
#     ans
#     result = bool


class UserInput(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    user_answer = models.IntegerField(Answer)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return "{0}, {1}".format(self.user, self.user_answer)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    date_of_birth = models.DateField()
    joining_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    level = models.ForeignKey(Level, default=1)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
