#!/usr/bin/env python

from twill import get_browser
from twill.commands import *
from re import match


def connect(url):
    b = get_browser()
    go(url)
    return b


def getLinks(b, urlfilter):
    #return None
    return [l for l in b._browser.links() if l.url.find(urlfilter) > -1]
    
   
def scrapeVisits(b, link):
    c_url = b.get_url()
    ex = ".*  (?P<vcount>[0-9]+)&nbsp;Views.*"
    b.follow_link(link)
    html = b.get_html().replace("\n", "")
    m = match(ex, html)
    if not m:
        print "can't find view count for %s" % link.text
        go(c_url)
        return -1
    else:
        go(c_url)    
        return m.groupdict()["vcount"]
    
   
    

filter = "/docs/DOC-"
murl = "http://community.zenoss.org/community/zenpacks"
b = connect(murl)
links = getLinks(b, filter)
all_visits = {}
for l in links:
    visits = scrapeVisits(b, l)
    all_visits[l.text] = visits
    
for l,v in all_visits.items():
    print "%s,%s" % (l, v)
    
   

    



"""
<span class="jive-content-footer-item">
            78803&nbsp;Views
        </span>
        
"""
