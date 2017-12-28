import requests
import argparse
from pprint import pprint
from datetime import datetime

# postgres imports
import os
from urllib import parse
import psycopg2

# set up postgres connection
if "DATABASE_URL" in os.environ:
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])

    # heroku prod database
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
else:
    # dev environment test database
    conn = psycopg2.connect(
        database='test',
        user='jcable',
        password='',
        host='localhost',
        port='',
    )

cur = conn.cursor()

# execute our Query
cur.execute("SELECT * FROM schedule_schedule")

# retrieve the records from the database
records = cur.fetchall()

for record in records:
    print("######################### RECORD")
    pprint(record)