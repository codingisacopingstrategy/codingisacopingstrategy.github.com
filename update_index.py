#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Update index.html by taking input from two sources:
http://schr.fr/
http://i.liketightpants.net/and/
"""

from time import strftime
from lxml import etree, html
from lxml.cssselect import CSSSelector
import re
import codecs
import feedparser

# Instead of using a template, we read in and update the existing file
htmltree = html.parse('index.html')

# Pull in syndication for the design portfolio
design_feed = feedparser.parse('http://schr.fr/feed')

# Pull in syndication for the blog
pants_feed = feedparser.parse('http://i.liketightpants.net/and/feed/us/recent_entries.xml')

# On the index page, find the list html element for design projects
# and clear the old values
sel = CSSSelector(".pagina2 dl")
design_dl = sel(htmltree)[0]
design_dl.clear()

# create the new html elements for design_dl and append them
for post in design_feed['items'][:4]:
    year = strftime( '%Y', post['updated_parsed'])
    dt = html.fragment_fromstring('<dt><a href="%s">%s</a> %s</dt>' % (post['link'], post['title'], year))
    try:
        # find the first image in the post’s content
        img = html.fragment_fromstring(post.content[0].value, "div").cssselect('img')[0]
        # it’s probably re-sized by WP to 620xsomething,
        # we need to make sure it displays at the size we want
        try:
            del img.attrib["height"]
        except KeyError:
            pass
        img.attrib['width'] = "264"
    except:
        continue
    design_dl.append(dt)
    dd = html.Element('dd')
    link = html.Element('a')
    link.attrib['href'] = post['link']
    link.append(img)
    dd.append(link)
    design_dl.append(dd)

sel = CSSSelector(".pagina3 dl")
pants_dl = sel(htmltree)[0]
pants_dl.clear()

# create the new html elements for pants_dl and append them
for post in pants_feed['items'][:5]:
    updated_formatted = strftime( '%B %d, %Y', post['updated_parsed'])
    dt = html.fragment_fromstring('<dt><a href="%s">%s</a> %s</dt>' % (post['link'], post['title'], updated_formatted))

    try:
        # find the first image in the post’s content
        img = html.fragment_fromstring(post.content[0].value, "div").cssselect('img')[0]
        # it’s probably sized at 830xsomething,
        # we need to make sure it displays at the size we want
        try:
            del img.attrib["height"]
        except KeyError:
            pass
        try:
            del img.attrib["style"]
        except KeyError:
            pass
        img.attrib['width'] = "264"
    except:
        continue

    dd = html.Element('dd')
    link = html.Element('a')
    link.attrib['href'] = post['link']
    link.append(img)
    dd.append(link)

    pants_dl.append(dt)
    pants_dl.append(dd)

# to debug
# print etree.tostring(design_dl, encoding='UTF-8', pretty_print=True)
# print etree.tostring(pants_dl, encoding='UTF-8', pretty_print=True)

with open('index.html', 'wb') as f:
    f.write(etree.tostring(htmltree, encoding='UTF-8', pretty_print=True))
    # print etree.tostring(htmltree, encoding='UTF-8', pretty_print=True)
