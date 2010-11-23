#!/usr/bin/python
#coding=utf-8
# author: notsobad
# I wrote this code to import google reader feed to my wordpress blog.

import xmlrpclib
from xml.dom import minidom
from pprint import pprint
import feedparser
import time
import sys, os

url = "http://blog.notsobad.cn/xmlrpc.php"
username = 'admin'
password = '*****'

def wp_post(serv, p):
    #url = "http://wxh/blog/xmlrpc.php"
    post = {
        'title' : "%s [zz]" % p['title'],
        'description' : '''<br/>From: <a href="%s" target="_blank">%s</a><br/>%s''' % (p['link'], p['author'], p['content']),
        'categories' : ['From web',]
    }
    #print post['title']
    #return
    id = serv.metaWeblog.newPost(1, username, password, post, 1)
    print "Add post %s, id is %s" % (post['title'], id)
    return int(id)

def check():
    recent = serv.mt.getRecentPostTitles(1, username, password, 10)
    for r in recent:
        print r['title']
            
    print recent

def _xml(end_link=None):
    
    # Change this to your feed
    url = "http://www.google.com/reader/public/atom/user%2F00404703289187651137%2Fstate%2Fcom.google%2Fbroadcast"
    d = feedparser.parse(url)

    print "updated at %s" % d['feed']['updated']
    new_end_link = d['entries'][0].get('link') or end_link
    
    posts = []
    for p in d['entries']:
        link = p.get('link')
        if link == end_link:
            break

        content = p.get('summary')
        if not content:
            content = p['content'][0].value

        posts.append({
            'title' : p.get('title'),
            'content' : content,
            'link' : link,
            'author' : p.get('author'),
        })
    # reverse, and newest on top
    posts.reverse()
    return (posts, new_end_link)

def do_post():
    try:
        f = open(".rpc_end_link", "r")
        end_link = f.read().strip()
        f.close()
    except IOError, e:
        print e
        #end_link = None
        print "Error of last url"
        sys.exit(1)


    posts, new_end_link = _xml(end_link)
    if not posts:
        print 'nothing new, quit'
        sys.exit(2)
    if new_end_link:
        f = open(".rpc_end_link", "w")
        f.write(new_end_link)
        f.close()
    for p in posts:
        wp_post(serv, p)
        time.sleep(1)
        

serv = xmlrpclib.Server(url)
   
if __name__== "__main__":
    do_post()
