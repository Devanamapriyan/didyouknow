#!/usr/bin/python

import urllib2
import json
#############################################################################
## RESTAPI KUNGFU BELOW
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
topic_list = {"user" : ["topicname"]}
content = {"user": {"topicname" : ["content"]}}
parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('topic_name')
parser.add_argument('topic_id')

class nextTopic(Resource):
     def get(self):
          username = request.args.get("username")
          topic_id = request.args.get("topic_id")
          d = topic_list[username][int(topic_id)]
          return d

class listAllTopic(Resource):
    def get(self):
         d = topic_list
         return d
    
class listUserTopic(Resource):
    def get(self):
         username = request.args.get("username")
         d = topic_list[username]
         return d
    
class delTopic(Resource):
    def delete(self):
         args = parser.parse_args()
         username = args['username']
         topic_id = args['topic_id']
         del(topic_list[username][int(topic_id)])
         d = topic_list[username]
         return d
    
class addTopic(Resource):
    def put(self):
         args = parser.parse_args()
         username = args['username']
         topic_name = args['topic_name']
         if username in topic_list:
              if topic_name not in topic_list[username]:
                   topic_list.setdefault(username,[]).append(topic_name)
              else:
                   return "!!Topic not added, Already In List!!"
         else:
              topic_list.setdefault(username,[]).append(topic_name)
         d = topic_list
         return d

api.add_resource(nextTopic, '/nextTopic')
api.add_resource(listAllTopic, '/listAllTopic')
api.add_resource(listUserTopic, '/listUserTopic')
api.add_resource(delTopic, '/delTopic')
api.add_resource(addTopic, '/addTopic')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8002)

## RESTAPI KUNGFU ABOVE
############################################################################

# to do : DB API for storing the topic name, wikipedia data and current location pointer.
# for now, lets simulate for a single case without db.

#####################################################


def addWikidata (topic_name):
     wikiname = topic_name + "_(disambiguation)"
     content = urllib2.urlopen("https://en.wikipedia.org/w/api.php?action=query&titles="+wikiname+"&prop=extracts&explaintext&format=json").read()
     result = json.loads(content)
     key = result['query']['pages'].keys()
     key = key[0]
     if (key == "-1"):
        result = "!! Error with the topic. No such topic found on wikipedia !!"
        return result
     result = "***************************************\n" + wikiname + "\n"
     result.append(result['query']['pages'][key]['extract'])
     (content[username][topic_name]).append(result)





