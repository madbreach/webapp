import secrets

from django.contrib import admin
from django.utils import timezone

from django.db import models


class Pronoun(models.Model):
    text = models.CharField(max_length=32)
    user_specified = models.BooleanField(default=False)

    def __str__(self):
        return self.text



class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    display_name = models.CharField(max_length=32, blank=True, default='')
    pronouns = models.ForeignKey(Pronoun, on_delete=models.RESTRICT)
    specified_pronouns = models.CharField(max_length=32, blank=True, default='')

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ('' if self.display_name == '' else ' (' + self.display_name + ')')


def makeTokenString():
    return secrets.token_urlsafe(27)


class JoinLink(models.Model):
    link = models.CharField(max_length=36, default=makeTokenString, unique=True, editable=False)
    link_creation_time = models.DateTimeField(default=timezone.now, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def full_link(self):
        return '/?t=' + self.link

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Program(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=128)
    zoom_link = models.CharField(max_length=128, default=None)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserSection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + ' in ' + self.section.__str__()


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)



def create_superuser_if_necessary():
    # Set the name and initial password you want the superuser to have here.
    # AFTER THIS SUPERUSER IS CREATED ON HEROKU, YOU ***MUST*** IMMEDIATELY CHANGE ITS PASSWORD
    # THROUGH THE ADMIN INTERFACE. (This password is stored in cleartext in a GitHub repository,
    # so it is not acceptable to use it when there is actual client data!)
    SUPERUSER_NAME = 'admin'
    SUPERUSER_PASSWORD = 'd38891b3'

    from django.contrib.auth.models import User

    if not User.objects.filter(username=SUPERUSER_NAME).exists():
        superuser = User(
            username=SUPERUSER_NAME,
            is_superuser=True,
            is_staff=True
        )

        superuser.save()
        superuser.set_password(SUPERUSER_PASSWORD)
        superuser.save()


# Once the superuser has been created on Heroku, you can comment out this line if you wish
# create_superuser_if_necessary()
