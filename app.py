#!/usr/bin/env python

import urllib
import json
import os
import MySQLdb

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

db=_mysql.connect(host="localhost", user="root", passwd="root", db="test_database")

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

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row)) 
            for row in cursor.fetchall()]

def makeWebhookResult(req):
    if req.get("result").get("action") != "find.name":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    surname = parameters.get("names")

    c=db.cursor()
    c.execute("""SELECT * FROM users""")

    results = dictfetchall(c)
    users = json.dumps(results)

    #users = {'Florian':'Adonis', 'Emna':'Bouzouita', 'Alex':'Guilngar'}

    speech = "The name of " + surname + " is " + str(users[surname]) + "."

    print("Response:")
    #print(speech)
    print(users)

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
