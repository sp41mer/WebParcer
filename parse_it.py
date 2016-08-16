# -*- coding: utf-8 -*-
__author__ = 'sp41mer'
from sources import connections, search_grabber,group_grabber, users_in_groups_parcer


def parse_it():
    connections.create_tables()
    search_grabber.get_groups('материнский капитал')
    group_grabber.write_to_cassandra_db()
    # users_in_groups_parcer.parce_users_from_groups()