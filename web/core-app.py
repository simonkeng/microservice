from flask import Flask
from flask import request
import logging
import psycopg2
import redis
import sys

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379)

# flask app logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)


def PgFetch(query, method):

    # connect to an existing database
    conn = psycopg2.connect(
        "host='postgres' dbname='core-app' user='postgres' password='dockerdemo'")

    # open a cursor to perform database operations
    cur = conn.cursor()

    # query db
    dbquery = cur.execute(query)

    if method == 'GET':
        result = cur.fetchone()
        print(f'GET request result: {result}')
    else:
        result = ""

    # make the changes to the database persistent
    conn.commit()

    cur.close()
    conn.close()

    print(f'Final result: {result}')
    return result


@app.route('/')
def hello_world():
    if cache.exists('visitor_count'):
        cache.incr('visitor_count')
        count = (cache.get('visitor_count')).decode('utf-8')
        update = PgFetch("UPDATE visitors set visitor_count = " +
                         count + " where site_id = 1;", "POST")
        print(f'Count value: {count}')

    else:
        cache_refresh = PgFetch(
            "SELECT visitor_count FROM visitors where site_id = 1;", "GET")
        try:
            count = int(cache_refresh[0])
            cache.set('visitor_count', count)
        except TypeError as err:
            if err == "'NoneType' object is not subscriptable":
                count = 0
                print('Custom exception caught..')

        cache.incr('visitor_count')
        count = (cache.get('visitor_count')).decode('utf-8')
        print(f'Count value: {count}')
    return f'This page has been viewed {count} time(s).'

@app.route('/resetcounter')
def resetcounter():

    cache.delete('visitor_count')
    PgFetch("UPDATE visitors set visitor_count = 0 where site_id = 1;", "POST")

    app.logger.debug("RESET VISITOR COUNT..")
    return "Successfully deleted redis and postgres counters"


@app.route('/pat', methods=['POST'])
def pat():
    first = request.args.get('first')
    last = request.args.get('last')
    return f'Hi {first} {last}, you are doing a great job today!'
