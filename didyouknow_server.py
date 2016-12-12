#!/usr/bin/python

import urllib2
import json
#############################################################################
## RESTAPI KUNGFU BELOW
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
topic_list = {}
topic_counter = 0

class nextTopic(Resource):
     def get(self, topic_id):
         return {topic_id: topic_list[topic_id]}
    
class listTopic(Resource):
    def get(self):
        return {topic_list}
    
class delTopic(Resource):
    def delete(self, topic_id):
        del(topic_list[topic_id])
        topic_counter--;
        return {topic_list}
    
class newTopic(Resource):
    def put(self, topic_name):
        topic_list[topic_counter++] = request.form['name']
        wikiname = topic + "_(disambiguation)"
        content = urllib2.urlopen("https://en.wikipedia.org/w/api.php?action=query&titles="+wikiname+"&prop=extracts&explaintext&format=json").read()
        result = json.loads(content)
        key = result['query']['pages'].keys()
        key = key[0]
        if (key == "-1"):
            print "Error with the topic. No such topic found on wikipedia!!"
            return -1
        print "***************************************\n" + wikiname + "\n"
        print result['query']['pages'][key]['extract'] 
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')
if __name__ == '__main__':
    app.run(debug=True)

## RESTAPI KUNGFU ABOVE
############################################################################

# to do : DB API for storing the topic name, wikipedia data and current location pointer.
# for now, lets simulate for a single case without db.

#####################################################





