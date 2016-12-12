#!/usr/bin/python

import urllib2
import json
#############################################################################
## RESTAPI KUNGFU BELOW
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
topic_list = {"user" : ["topicname"]}
content = {"user": {"topicname" : ["content"]}}
parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('topic_name')


class nextTopic(Resource):
     def get(self):
         return {topic_id: topic_list[username][topic_id]}

class listAllTopic(Resource):
    def get(self):
        return {topic_list}
    
class listUserTopic(Resource):
    def get(self):
        return {topic_list[username]}
    
class delTopic(Resource):
    def delete(self):
        username = request.form['username']
        topic_id = request.form['topic_id']
        del(topic_list[username][topic_id])
        return {topic_list[username]}
    
class addTopic(Resource):
    def put(self):
        username = request.form['username']
        topic_name = request.form['topic_name']
        (topic_list[username]).append(topic_name)
        wikiname = topic_name + "_(disambiguation)"
        content = urllib2.urlopen("https://en.wikipedia.org/w/api.php?action=query&titles="+wikiname+"&prop=extracts&explaintext&format=json").read()
        result = json.loads(content)
        key = result['query']['pages'].keys()
        key = key[0]
        if (key == "-1"):
            print "Error with the topic. No such topic found on wikipedia!!"
            return -1
        result = "***************************************\n" + wikiname + "\n"
        result.append(result['query']['pages'][key]['extract'])
        (content[username][topic_name]).append(result)
        return {topic_list[username]}

api.add_resource(nextTopic, '/next')
api.add_resource(listAllTopic, '/listAllTopic')
api.add_resource(listUserTopic, '/listUserTopic')
api.add_resource(delTopic, '/delTopic')
api.add_resource(nextTopic, '/addTopic')

if __name__ == '__main__':
    app.run(debug=True)

## RESTAPI KUNGFU ABOVE
############################################################################

# to do : DB API for storing the topic name, wikipedia data and current location pointer.
# for now, lets simulate for a single case without db.

#####################################################





