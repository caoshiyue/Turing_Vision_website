##
# Author:
# Description:
# LastEditors: Shiyuec
# LastEditTime: 2021-12-02 21:15:04
##
from django.db import models
# Create your models here.
from django.utils.timezone import now
import os
import json


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
    human=models.BooleanField()
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
    firstname = models.CharField(blank=True, null=True, max_length=64)
    lastname = models.CharField(blank=True, null=True, max_length=64)
    url = models.CharField(blank=True, null=True, max_length=256)
    affiliation = models.CharField(blank=True, null=True, max_length=64)
    registration_time = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
