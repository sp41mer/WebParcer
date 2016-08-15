__author__ = 'sp41mer'
import json, requests, sys, logging, time, datetime
from models import GroupNoSQL, FriendsNoSQL, User, Group
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from vk_access_token import vk_access_token

fields = 'exports,personal,occupation,connections,sex,country,city,' \
         'bdate,sex,deactivated,has_photo,contacts,status,last_seen,' \
         'followers_count,online,relation,interests'

connection.setup(['127.0.0.1'], "mykeyspace", protocol_version=3)
for group in Group.select().limit(20):
    group_id = group.vk_id
    q = GroupNoSQL.objects(vk_id=group_id)

    for info in q[0].members:
        #grabbing friends to Cassandra
        method = "friends.get"
        user_id = info
        response = requests.post('https://api.vk.com/method/' + method,
                                 data={'user_id': user_id})
        data = json.loads(response.text)
        try:
            friends = data['response']
            FriendsNoSQL.create(vk_id=str(user_id), friends=friends)
        except Exception:
            print str(user_id)+' '+data['error']['error_msg']
        #grab info to PotsgresSQL
        method = "users.get"
        response = requests.post('https://api.vk.com/method/' + method,
                                 data={'user_id': user_id,
                                       'fields': fields,
                                       'v': 5.53,
                                       'access_token': vk_access_token})
        data = json.loads(response.text)
        try:
            info = data['response']
            a = User(
                vk_id=info[0].get('uid', None),
                first_name=info[0].get('first_name', None),
                last_name=info[0].get('last_name', None),
                sex=info[0].get('sex', None),
                bdate=info[0].get('bdate', None),
                status=info[0].get('status', None),
                deactivated=info[0].get('deactivated', None),
                has_photo=info[0].get('has_photo', None),
                mobile_phone=info[0].get('mobile_phone', None),
                home_phone=info[0].get('home_phone', None),
                skype=info[0].get('skype', None),
                facebook=info[0].get('facebook', None),
                twitter=info[0].get('twitter', None),
                livejournal=info[0].get('livejournal', None),
                instagram=info[0].get('instagram', None),
                political=info[0].get('political', None),
                religion=info[0].get('religion', None),
                people_main=info[0].get('people_main', None),
                life_main=info[0].get('life_main', None),
                smoking=info[0].get('smoking', None),
                alcohol=info[0].get('alcohol', None),
                inspired_by=info[0].get('inspired_by', None),
                online=info[0].get('online', None),
                online_app=info[0].get('online_app', None),
                online_mobile=info[0].get('online_mobile', None),
                relation=info[0].get('relation', None),
                interests=info[0].get('interests', None),
                country_id=info[0].get('country', None),
                city_id=info[0].get('city', None)
            )
            if info[0].get('occupation', None):
                    a.occupation_type = info[0].get('occupation').get('type', None)
                    a.occupation_id = info[0].get('occupation').get('id', None)
                    a.occupation_name = info[0].get('occupation').get('name', None)
            if info[0].get('last_seen', None):
                a.last_seen_time = info[0].get('last_seen').get('time', None)
                a.last_seen_platform = info[0].get('last_seen').get('platform', None)
                a.save()
                print info[0].get('last_name', None)
        except Exception, e:
            print str(e)
            print data
        time.sleep(0.4)

