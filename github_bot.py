from flask import Flask, request, abort
import json 
import urllib2
import hmac
import hashlib

app = Flask(__name__)

#Secret provided in the Github webhook config
SECRET_TOKEN = "EventsToSparkRoom"

@app.route('/', methods =['POST'])


def githubCommits():
    # This function validates if the request is properly signed by Github.
    # Then collects the webhook payload sent from Github and parses the parameters you want to send to Spark Room.

    headers = request.headers
    incoming_signature = headers.get('X-Hub-Signature')
    signature = 'sha1=' + hmac.new(SECRET_TOKEN, request.data, hashlib.sha1).hexdigest()
    
    if incoming_signature is None:
       abort(401)
    
    elif signature == incoming_signature:
        
        json_file = request.json
        
        if 'push' == headers.get('X-GitHub-Event'):
            commit = json_file['commits'][0]
            commit_id = commit['id']
            commit_message = commit['message']
            commit_time = commit['timestamp']
            commit_url = commit['url']
            commit_author_name = commit['author']['name']
            committer_name = commit['committer']['name']
            pusher_name = json_file['pusher']['name']
            repo_name = json_file['repository']['name']
            results = """**Author**: {0}\n\n**Committer**: {1}\n\n**Pusher**: {2}\n\n**Commit Message**: {3}\n\n**Commit id**: {4}\n\n**Time**: {5}\n\n**Repository**: {6}\n\n**Commit Link**: {7}<br><br>""".format(commit_author_name,committer_name,pusher_name,commit_message,commit_id,commit_time,repo_name,commit_url)
            toSpark(results)
            return 'Ok'

    else:
        print ("Fake Hook")
        abort(401)

# GET Function that gets user's room id that the bot is added to 
def getRoomId():
    

# POST Function  that sends the commits & posts it to Spark room  
def toSpark(commits):
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {'accept':'application/json','Content-Type':'application/json','Authorization': 'Bearer MTM2Y2I3MDctNDcwOS00MmI1LTliZDUtMDAxZmVjODE3MzRmYzdlYTMzNWQtYTU5'}
    values =   {'roomId':'Y2lzY29zcGFyazovL3VzL1JPT00vM2MzMzk4MmYtNzQ2Yi0zNzNjLWEwNTItM2M1MDg5MWU0NDYw', 'markdown': commits }
    
    #mine 
    #Y2lzY29zcGFyazovL3VzL1JPT00vM2MzMzk4MmYtNzQ2Yi0zNzNjLWEwNTItM2M1MDg5MWU0NDYw
    #john
    #Y2lzY29zcGFyazovL3VzL1JPT00vOGYxOGYwNzAtNzAyNC0xMWU4LWJhNDYtZTk5NjdlOThmOGM2
    data = json.dumps(values)
    req = urllib2.Request(url = url , data = data , headers = headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080, debug=True)
