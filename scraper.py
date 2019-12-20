#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module docstring: One line description of what your program does.

There should be a blank line in between description above, and this
more detailed description. In this section you should put any caveats, 
environment variable expectations, gotchas, and other notes about running
the program.  Author tag (below) helps instructors keep track of who 
wrote what, when grading.
"""
__author__ = 'ericmhanson'

import sys
import requests
import re
from html.parser import HTMLParser
import pprint

re_url = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
re_email = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
re_phone = r'(1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?)'


class MyHTMLParser(HTMLParser):
    a_link_list = []
    img_link_list = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.a_link_list.append(value)
        if tag == 'img':
            for attr, value in attrs:
                if attr == 'src':
                    self.img_link_list.append(value)


def main(args):
    """Main function is declared as standalone, for testability"""
    good_phone_list = []
    url = args[0]
    response = requests.get(url)
    response.raise_for_status()
    url_list = set(re.findall(re_url, response.text))
    email_list = set(re.findall(re_email, response.text))
    bad_phone_list = set(re.findall(re_phone, response.text))
    for phone in bad_phone_list:
        good_phone_list.append(phone[1] + phone[2] + phone[3])
    print('\nURLs:\n\n')
    pprint.pprint(url_list)
    print('\nEmails:\n\n')
    pprint.pprint(email_list)
    print('\nPhone numbers:\n\n')
    pprint.pprint(good_phone_list)
    
    parser = MyHTMLParser()
    parser.feed(response.text)
    print('\nA tag links:\n\n')
    pprint.pprint(set(parser.a_link_list))
    print('\nIMG links:\n\n')
    pprint.pprint(set(parser.img_link_list))


if __name__ == '__main__':
    main(sys.argv[1:])