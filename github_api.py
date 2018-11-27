import urllib
import json
import statistics
from datetime import datetime
import requests
#Get contributors list with additions, deletions, and commit counts
def getContributions(username, reponame):
    urlreq = urllib.request.urlopen("http://api.github.com/repos/" + username + "/" + reponame + "/stats/contributors")
    data = json.loads(str(urlreq.read().decode('utf-8')))
    count = 0
    count_contributors = 0
    countmax = 0
    
    for obj in data:
        n = int(obj['total'])
        count = count + n
        if n > countmax:
            countmax = n
    
    urlreq = urllib.request.urlopen("http://api.github.com/repos/" + username + "/" + reponame + "/contributors")
    data = json.loads(str(urlreq.read().decode('utf-8')))
    
    info = urlreq.info()
  
    sindex = info['Link'].index('page=', info['Link'].index('rel="next"')) + 5
    
    last = 0
    
    while(info['Link'][sindex].isdigit()):
      last = last * 10 + int(info['Link'][sindex])
      sindex += 1
    
    #print(last)
    urlreq = urllib.request.urlopen("http://api.github.com/repos/" + username + "/" + reponame + "/contributors?page=" + str(last))
    data = json.loads(str(urlreq.read().decode('utf-8')))
    #print(len(data))
    count_contributors = (last - 1) * 30 + len(data)

    return count, countmax, count_contributors

def iCTHelper(issues):
  times = []
  for issue in issues:
    t1 = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    t2 = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
    
    diff = t2 - t1
    diff = (diff.days * 24 * 60 * 60) + (diff.seconds)
      
    times.append(diff)
  return times
  
def issueCloseTimes():
  times = []
  
  
  urlreq = requests.get("http://api.github.com/repos/MicroPyramid/Django-CRM/issues?state=closed", auth=("paragverma", "pass1234"))
  data = json.loads(str(urlreq.content.decode('utf-8')))
  info = urlreq.headers
  
  sindex = info['Link'].index('page=', info['Link'].index('rel="next"')) + 5
  
  last = 0
  
  while(info['Link'][sindex].isdigit()):
    last = last * 10 + int(info['Link'][sindex])
    sindex += 1
  
  times.extend(iCTHelper(data))
  
  for i in range(2, last + 1):
    print(i)
    urlreq = requests.get("http://api.github.com/repos/MicroPyramid/Django-CRM/issues?state=closed&page=" + str(i), auth=("paragverma", "pass1234"))
    data = json.loads(str(urlreq.content.decode('utf-8')))
    times.extend(iCTHelper(data))
    
    
  
  return times, statistics.mean(times), statistics.median(times)

def getCommitCount(username, reponame):
  count = 0
  urlreq = urllib.request.urlopen("http://api.github.com/repos/" + username + "/" + reponame + "/commits")
  #data = json.loads(str(urlreq.read().decode('utf-8')))
  info = urlreq.info()
  
  sindex = info['Link'].index('page=', info['Link'].index('rel="next"')) + 5
  
  last = 0
  
  while(info['Link'][sindex].isdigit()):
    last = last * 10 + int(info['Link'][sindex])
    sindex += 1
  
  urlreq = urllib.request.urlopen("http://api.github.com/repos/" + username + "/" + reponame + "/commits?page=" + str(last) + "&per_page=1000")
  data = json.loads(str(urlreq.read().decode('utf-8')))
  
  return (last - 1) * 30 + len(data)
  
  count += len(data)
  
  sindex = urlreq.info()['Link'].index('rel="last"')
      
  #print(data)
  return count

#MicroPyramid/Django-CRM/
username = 'MicroPyramid'
reponame = 'Django-CRM'
