# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Sleeps(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(unique=True, blank=True, null=True)
    wake = models.IntegerField(blank=True, null=True)
    bath = models.IntegerField(blank=True, null=True)
    bed = models.IntegerField(blank=True, null=True)
    sleep_in = models.CharField(max_length=255, blank=True, null=True)
    sleep = models.CharField(max_length=255, blank=True, null=True)
    deep_sleep = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sleeps'

class SleepProspects(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField(blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sleep_prospects'

class DeepSleepProspects(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField(blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'deep_sleep_prospects'

class Percent():
    per_year=[]
    per_season=[]
    per_month=[]
    per_week=[]
