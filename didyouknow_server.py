#!/usr/bin/python

import urllib2
import json
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def delete(self, todo_id):
        todos[todo_id] = ""
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
    

##topic = "docker_(disambiguation)"
###topic = "Docker_(software)"
##
##content = urllib2.urlopen("https://en.wikipedia.org/w/api.php?action=query&titles="+topic+"&prop=extracts&explaintext&format=json").read()
###print content
##
##
##result = json.loads(content)
##
##key = result['query']['pages'].keys()
##key = key[0]
##
##print topic + "\n"
##print result['query']['pages'][key]['extract']





def get_Correct_Topic () :
    topic = "docker_(disambiguation)"
    #topic = "Docker_(software)"

    content = urllib2.urlopen("https://en.wikipedia.org/w/api.php?action=query&titles="+topic+"&prop=extracts&explaintext&format=json").read()
    #print content


    result = json.loads(content)

    key = result['query']['pages'].keys()
    key = key[0]

    print topic + "\n"
    print result['query']['pages'][key]['extract']


