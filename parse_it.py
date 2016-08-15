__author__ = 'sp41mer'
from sources import connections, search_grabber


def parse_it(query):
    connections.create_tables()
    search_grabber.get_groups(query)