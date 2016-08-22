__author__ = 'sp41mer'
from models import *
import peewee, globals
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.auth import PlainTextAuthProvider

database = peewee.PostgresqlDatabase(
    globals.postgres_database,
    user=globals.postgres_user,
    password=globals.postgres_password,
    host=globals.postgres_database
)

def create_tables():
    database.connect()
    try:
        database.create_tables([User, Group], True)
    except Exception, e:
        print str(e)

def connect_and_sync(models):
    #if localhost
    connection.setup(globals.cassandra_host, globals.cassandra_keyspace, globals.cassandra_protocol_version)
    #if Digital Ocean
    # auth_provider = PlainTextAuthProvider(username=globals.cassandra_username, password=globals.cassandra_password)
    # connection.setup([globals.cassandra_host, globals.cassandra_keyspace, globals.cassandra_protocol_version, auth_provider=auth_provider)
    for model in models:
        sync_table(model)