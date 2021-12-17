##
# Author:
# Description:
# LastEditors: Shiyuec
# LastEditTime: 2021-12-17 22:08:17
##
from django.db import models
# Create your models here.
from django.utils.timezone import now
import turingvision.settings
from django import forms
from django.core.mail import send_mass_mail
from django.conf import settings as settings
from django.core.mail import EmailMultiAlternatives
import hashlib


class AlembicVersion(models.Model):
    version_num = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class Downloads(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, blank=True, null=True, max_length=64)
    counts = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'downloads'


class Submissions(models.Model):
    id = models.AutoField(primary_key=True)
    human = models.BooleanField()
    modelname = models.CharField(blank=True, null=True, max_length=16)
    description = models.CharField(blank=True, null=True, max_length=256)
    ap = models.FloatField(blank=True, null=True)
    ap50 = models.FloatField(blank=True, null=True)
    ap75 = models.FloatField(blank=True, null=True)
    aps = models.FloatField(blank=True, null=True)
    apm = models.FloatField(blank=True, null=True)
    apl = models.FloatField(blank=True, null=True)
    submission_url = models.CharField(
        unique=True, blank=True, null=True, max_length=128)
    paper_url = models.CharField(
        unique=True, blank=True, null=True, max_length=128)
    hardware = models.CharField(blank=True, null=True, max_length=32)
    timestamp = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submissions'


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, blank=True, null=True, max_length=64)
    username = models.CharField(
        unique=True, blank=True, null=True, max_length=64)
    password_hash = models.CharField(blank=True, null=True, max_length=128)
    confirmed = models.BooleanField(blank=True, null=True)
    registration_time = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class login_form(forms.Form):
    email = forms.CharField(label="email", max_length=64)
    password = forms.CharField(
        label="password", max_length=256, widget=forms.PasswordInput)


class register_form(forms.Form):
    username = forms.CharField(label="email", max_length=64)
    email = forms.CharField(label="email", max_length=64)
    password = forms.CharField(
        label="password", max_length=256, widget=forms.PasswordInput)


def send_email(usr, email):
    subject = 'TuringVision register confirm'
    with open('static/email/confirm.txt', 'r') as f:
        text_content = f.read()
    with open('static/email/confirm.html', 'r') as f:
        html_content = f.read()
    text_content = text_content.replace('$usr', usr)
    html_content = html_content.replace('$usr', usr)
    m = hashlib.md5(email.encode())
    link = settings.HOST+'/register_confirm/?user='+usr+'&token='+m.hexdigest()
    text_content = text_content.replace('$link', link)
    html_content = html_content.replace('$link', link)
    msg = EmailMultiAlternatives(
        subject, text_content, 'TuringVision <turingvision@163.com>', [email])

    msg.attach_alternative(html_content, "text/html")
    msg.send()
