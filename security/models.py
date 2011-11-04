from django.db import models

class DmcaNotifications(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.IntegerField()
    ip = models.IntegerField()
    port = models.IntegerField()
    mac_address = models.CharField(max_length=51)
    onid_username = models.CharField(max_length=51, blank=True)
    network = models.CharField(max_length=51)
    material = models.CharField(max_length=1536)
    zone = models.CharField(max_length=90)
    notification_id = models.CharField(max_length=42)
    violation_id = models.IntegerField(null=True, blank=True)
    failed = models.IntegerField()
    host = models.CharField(max_length=384, blank=True)
    domain = models.CharField(max_length=765, blank=True)
    owning_unit = models.CharField(max_length=384, blank=True)
    user_id = models.CharField(max_length=384, blank=True)
    department = models.CharField(max_length=384, blank=True)
    class Meta:
        db_table = u'dmca_notifications'

class DmcaViolations(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.IntegerField()
    onid_username = models.CharField(max_length=60, blank=True)
    zone = models.CharField(max_length=60, blank=True)
    quiz_completion = models.IntegerField(null=True, blank=True)
    disabled = models.CharField(max_length=1)
    offense_number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'dmca_violations'

class DmcaViolationsArchive(models.Model):
    id = models.IntegerField(primary_key=True)
    old_id = models.IntegerField()
    time = models.IntegerField()
    onid_username = models.CharField(max_length=96, blank=True)
    zone = models.CharField(max_length=60, blank=True)
    quiz_completion = models.IntegerField(null=True, blank=True)
    disabled = models.CharField(max_length=1)
    offense_number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'dmca_violations_archive'

class DmcaNotificationsArchive(models.Model):
    id = models.IntegerField(primary_key=True)
    old_id = models.IntegerField()
    time = models.IntegerField()
    ip = models.IntegerField()
    mac_address = models.CharField(max_length=96)
    onid_username = models.CharField(max_length=96, blank=True)
    network = models.CharField(max_length=51)
    material = models.CharField(max_length=1536)
    zone = models.CharField(max_length=90)
    notification_id = models.CharField(max_length=42)
    violation_id = models.IntegerField(null=True, blank=True)
    failed = models.IntegerField()
    class Meta:
        db_table = u'dmca_notifications_archive'

class FireeyeNotifications(models.Model):
    id = models.IntegerField(primary_key=True)
    latest_activity = models.IntegerField()
    ip = models.IntegerField()
    hostname = models.CharField(max_length=150, blank=True)
    mac_address = models.CharField(max_length=51)
    onid_username = models.CharField(max_length=51, blank=True)
    zone = models.CharField(max_length=150)
    malware = models.CharField(max_length=105, blank=True)
    callback_ip = models.CharField(max_length=105, blank=True)
    hits = models.IntegerField()
    time_emailed = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'fireeye_notifications'
