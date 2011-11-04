from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Count
from netshed.security.models import DmcaNotifications, DmcaNotificationsArchive
from netshed.security.models import DmcaViolations, DmcaViolationsArchive
from netshed.security.models import FireeyeNotifications
import datetime
import time

def index(request): 
    """ Security report, aggregate statistics for current year and all time """

    start_year_timestamp = time.mktime(time.strptime(str(datetime.datetime.today().year) + '0101', '%Y%m%d'))

    # Get dmca notifications grouped by zone for current year
    notifications_year = DmcaNotifications.objects.using('dmca').values('zone').filter(time__gte=start_year_timestamp).annotate(count=Count('zone')).order_by('count').reverse()

    # Get dmca notifications grouped by zone for all time
    notifications = list(DmcaNotifications.objects.using('dmca').values('zone').annotate(count=Count('zone')))
    notifications_archive = list(DmcaNotificationsArchive.objects.using('dmca').values('zone').annotate(count=Count('zone')))
    notifications_all = dict_merge_sort(notifications, notifications_archive)

    # Get number of repeat offenders by zone for current year 
    repeat_year = DmcaViolations.objects.using('dmca').values('zone').filter(time__gte=start_year_timestamp, offense_number__gt=1).annotate(count=Count('zone')).order_by('count').reverse()

    # Get number of repeat offenders by zone for all time
    repeat_offenders = list(DmcaViolations.objects.using('dmca').values('zone').filter(offense_number__gt=1).annotate(count=Count('zone')).order_by('count').reverse())
    repeat_offenders_archive = list(DmcaViolationsArchive.objects.using('dmca').values('zone').filter(offense_number__gt=1).annotate(count=Count('zone')).order_by('count').reverse())
    repeat_all = dict_merge_sort(repeat_offenders,repeat_offenders_archive)

    # Get number of fireeye notifications grouped by zone for all time 
    fireeye_all = FireeyeNotifications.objects.using('net').values('zone').annotate(count=Count('zone')).order_by('count').reverse() 

    return render_to_response('security/index.html', {'repeat_year':repeat_year, 'repeat_all':repeat_all, 'notifications_year':notifications_year, 'notifications_all':notifications_all, 'fireeye_all':fireeye_all})

def dict_merge_sort(a, b):
    """ Two list of dicts into one sorted list by combining values """

    c = []
    for elem in b:
        a.append(elem)
    for elem in a:
        if elem['zone'] not in [zone_count['zone'] for zone_count in c]:
            c.append(elem)
        else:
            for zone_count in c:
                if elem['zone'] == zone_count['zone']:
                    zone_count['count'] += elem['count']
    return sorted(c, key=lambda zone_count:zone_count['count'], reverse=True)

        
            
        
        
