__author__ = 'sp41mer'
import json, requests, sys, logging, time, datetime
from models import GroupNoSQL, FriendsNoSQL, User, Group
import connections
from vk_access_token import vk_access_token


def write_to_cassandra_db():
    connections.connect_and_sync([GroupNoSQL, FriendsNoSQL])

    for group in Group.select():
        method = "groups.getMembers"
        group_id = str(group.vk_id)
        preresponse = requests.post('https://api.vk.com/method/' + method,
                                data={'group_id': group_id,
                                      'sort': 'id_asc',
                                      'offset': 0,
                                      'count': 1000,
                                      'v': 5.53,
                                      'access_token': vk_access_token})
        predata = json.loads(preresponse.text)
        counter = predata['response']['count']
        data = predata['response']['items']
        times = (counter // 1000)+1
        if times > 1:
            for i in range(1, times):
                response = requests.post('https://api.vk.com/method/' + method,
                                    data={'group_id': group_id,
                                          'sort': 'id_asc',
                                          'offset': 1000*i,
                                          'count': 1,
                                          'v': 5.53,
                                          'access_token': vk_access_token})
                jsondata = json.loads(response.text)
                data = data + jsondata['response']['items']
                time.sleep(0.4)
        try:
            GroupNoSQL.create(vk_id=group_id, members=set(data))
        except Exception, e:
            print str(e)
            print predata
        print group.name
        time.sleep(0.4)


