from flask import Flask
from flask import request, render_template
import logging
import psycopg2
import redis
import sys
import requests

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

# postres interface
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
def page_view_counter():

    if cache.exists('visitor_count'):
        cache.incr('visitor_count')
        count = (cache.get('visitor_count')).decode('utf-8')
        update = PgFetch(
            "UPDATE visitors set visitor_count = " +
            count + " where site_id = 1;", "POST"
        )
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
    return f'<h1>This page has been viewed {count} time(s).</h1>'


@app.route('/resetcounter')
def resetcounter():
    # reset redis
    cache.delete('visitor_count')
    # update postgres
    PgFetch("UPDATE visitors set visitor_count = 0 where site_id = 1;", "POST")
    app.logger.debug("\nRESET VISITOR COUNT\n")
    return "<h1>Successfully deleted redis and postgres counters</h1>"


@app.route('/pat', methods=['GET', 'POST'])
def pat():
    first = request.args.get('first')
    last = request.args.get('last')
    return f'<h2><marquee>Hi {first} {last}, you are doing a great job today!</marquee></h2>'


@app.route('/cat')
def cat():
    return render_template('cat.html')


@app.route('/call_api', methods=['GET'])
def call_api():
    r = requests.get('http://api:8001/return_data')
    print(r.status_code)
    return f'<h3>Call result {r.text}</h3>'
