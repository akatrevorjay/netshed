from django.db import models

class Greylist(models.Model):
    ip = models.CharField(max_length=48, primary_key=True)
    sender = models.CharField(max_length=255, primary_key=True)
    recipient = models.CharField(max_length=255, primary_key=True)
    first = models.IntegerField()
    last = models.IntegerField()
    n = models.IntegerField()
    class Meta:
        db_table = u'greylist'

class Whitelist(models.Model):
    mail = models.CharField(max_length=255, primary_key=True)
    comment = models.CharField(max_length=726)
    class Meta:
        db_table = u'whitelist'
