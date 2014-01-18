'''
Created on Apr 30, 2013

@author: afzal
'''
import scraperwiki
import simplejson
import sys
import urllib2
import requests
import json

RESULTS_PER_PAGE = '10'
LANGUAGE = 'en'
NUM_PAGES = 1

TNAME = 'concert'
LON = '-79.9279'
LAT = '43.2596'

s = requests.Session()

for page in range(1, NUM_PAGES+1):
    base_url = 'http://api.seatgeek.com/2/events?taxonomies.name=%s&lon=%s&lat=%s' \
        % (urllib2.quote(TNAME), urllib2.quote(LON), urllib2.quote(LAT))
    try:
        results_json = simplejson.loads(scraperwiki.scrape(base_url))

    except:
        print sys.exc_info()[0]
        print 'Oh dear, failed to scrape %s' % base_url


    events = {}
    events_arr = []

    headers = {'Authorization': 'EL4GqpALoi1KWBgTYBYEfBWLKTJXAxKAR7r57jPl'}

    for result in results_json['events']:
        data = {}
        data['sg_id'] = result['id']
        data['short_title'] = result['short_title']
        data['datetime_local'] = result['datetime_local']
        data['datetime_utc'] = result['datetime_utc']
        data['place'] = result['venue']['name']
        data['address'] = str(result['venue']['extended_address'])
        data['banner_img'] = str(result['performers'][0]['image'])
        events_arr.append(data)

    events['events'] = json.dumps(events_arr)
    # print events
    r = s.post("http://vv.api/admin/events/events", data=events, headers=headers)

    print r.text
