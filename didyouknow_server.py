#!/usr/bin/python

import json
import urllib2
import os
import re
#############################################################################
## RESTAPI KUNGFU BELOW
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
topic_list = {"user" : ["topicname"]}
content_list = {}
parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('topic_name')
parser.add_argument('topic_id')

def urlify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)
    return s
     

def addWikidata (username,topic_name):
     content = urllib2.urlopen("https://en.wikipedia.org/w/api.php?action=opensearch&search="+topic_name+"&limit=20&namespace=0&format=jsonfm").read()
    #  key = key[0]
    #  if (key == "-1"):
    #     result = "!! Error in adding the topic. No such topic found on wikipedia !!"
    #     topic_list[username].remove(topic_name)
    #     return result
     content_tmp = { username: { topic_name: [content]}}
     content_list.update(content_tmp)
     return content_list[username][topic_name]

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
         username = str(args['username']).lower()
         topic_name = str(args['topic_name']).lower()
         username = urlify(username)
         topic_name = urlify(topic_name)
         if username in topic_list:
              if topic_name not in topic_list[username]:
                   topic_list.setdefault(username,[]).append(topic_name)
                   d=addWikidata(username,topic_name)
              else:
                   d="!!Topic not added, Already In List!!"
         else:
              topic_list.setdefault(username,[]).append(topic_name)
              d=addWikidata(username,topic_name)
         #d = topic_list
         return d

api.add_resource(nextTopic, '/nextTopic')
api.add_resource(listAllTopic, '/listAllTopic')
api.add_resource(listUserTopic, '/listUserTopic')
api.add_resource(delTopic, '/delTopic')
api.add_resource(addTopic, '/addTopic')

if __name__ == '__main__':
    IP="0.0.0.0"
    PORT=os.getenv("PORT")
    app.run(debug=True,host=IP, port=int(PORT))

## RESTAPI KUNGFU ABOVE
    
############################################################################
# To do:    
# Better error condition checks and boundary cases to be caught.
# Add content from wikipedia in a different structure called "content"
# link this content with the nextTopic, delTopic and addTopic functions 
#####################################################









