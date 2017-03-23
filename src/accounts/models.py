from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class Level(models.Model):
    """All Levels are saved here"""
    level_name = models.CharField(max_length=120)
    def __unicode__(self):
        return self.level_name


class Question(models.Model):
    """All Questions are saved here"""
    question_content = models.TextField()
    level = models.ForeignKey(Level)

    def __unicode__(self):
        return self.question_content


class Answer(models.Model):
    """All options are saved here"""
    answer_content = models.TextField()
    question = models.ForeignKey(Question, related_name="qus")
    is_correct = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.answer_content


class UserInput(models.Model):
    """User Inputs are saved here"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    level = models.ForeignKey(Level, default=1)
    question = models.ForeignKey(Question, default=1)
    user_answer = models.IntegerField(Answer)
    score = models.IntegerField(default=0)
    
    def __unicode__(self):
        return "{0}, {1}".format(self.user, self.user_answer)


class ImageDescModel(models.Model):
    """Image upload form."""
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    level = models.ForeignKey(Level, default=1)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.description


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
    LEVEL_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    date_of_birth = models.DateField()
    joining_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    level_one = models.CharField(max_length=1, choices=LEVEL_CHOICES, default='N')
    level_two= models.CharField(max_length=1, choices=LEVEL_CHOICES, default='N')
    level_three = models.CharField(max_length=1, choices=LEVEL_CHOICES, default='N')
 
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
