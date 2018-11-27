try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import urllib.request as conn
import requests
from tidylib import tidy_document
from datetime import datetime, timedelta

def getTimes(page=1):
  global_list = []
  part1 = "http://code.vtiger.com/vtiger/vtigercrm/issues?assignee_id=&author_id=&label_name=&milestone_id="
  part2 = "&page="
  part3 = "&scope=all&sort=created_desc&state=closed"
  
  print(page)
  if page == 1:
    data = conn.urlopen(part1 + part3)
  else:
    data = conn.urlopen(part1 + part2 + str(page) + part3)
  
  html = data.read().decode(data.info().get_param('charset') or 'utf-8')
  document, errors = tidy_document(html)
  
  parsed_html = BeautifulSoup(document)
  
  l1 = parsed_html.body.find('div', attrs={'class':'page-sidebar-expanded page-with-sidebar'})
  l2 = l1.find('div', attrs={'class':'content-wrapper'})
  l3 = l2.find('div', attrs={'class':'container-fluid'})
  l4 = l3.find('div', attrs={'class':'content'})
  l5 = l4.find('div', attrs={'class':'clearfix'})
  l6 = l5.find('div', attrs={'class':'issues-holder'})
  l7 = l6.find('div', attrs={'class':'panel panel-default'})
  l8 = l7.find('ul', attrs={'class':'well-list issues-list'})
  
  for li in l8.contents:
    if len(li) > 1:
      l9 = li.find('div', attrs={'class':'issue-info'})
      t1 = datetime.strptime(l9.time.attrs['datetime'], '%Y-%m-%dT%H:%M:%SZ')
      
      l10 = li.find('div', attrs={'class':'pull-right issue-updated-at'})
      t2 = datetime.strptime(l10.small.time.attrs['datetime'], '%Y-%m-%dT%H:%M:%SZ')
      
      diff = t2 - t1
      diff = (diff.days * 24 * 60 * 60) + (diff.seconds)
      
      global_list.append(diff)
  
  return global_list

times = []

for i in range(1, 40 + 1):
  times.extend(getTimes(page=i))