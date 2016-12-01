#!/usr/bin/env python

import urllib
import json
import os
import psycopg2
import urlparse

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["postgres://mumspcihucbpgc:qyCb-fkcxCAu25CKCcvqfgPQI2@ec2-54-217-214-51.eu-west-1.compute.amazonaws.com:5432/dble4c6c3gvjsu"])

if (
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)):
    ok=1
else:
    ok=0

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#def dictfetchall(cursor):
    #"""Returns all rows from a cursor as a list of dicts"""
    #desc = cursor.description
    #return [dict(itertools.izip([col[0] for col in desc], row)) 
    #        for row in cursor.fetchall()]

def makeWebhookResult(req):
    if req.get("result").get("action") != "find.name":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    surname = parameters.get("names")

    #c=db.cursor()
    #c.execute("""SELECT * FROM users""")

    #results = dictfetchall(c)
    #users = json.dumps(results)


    users = {'Florian':ok, 'Emna':'Bouzouita', 'Alex':'Guilngar'}

    speech = "The name of " + surname + " is " + str(users[surname]) + "."

    print("Response:")
    print(speech)
    #print(users)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
