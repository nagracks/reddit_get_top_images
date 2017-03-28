#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "nagracks"
__date__      = "13-08-2016"
__license__   = "MIT"
__copyright__ = "Copyright © 2016 nagracks"

import os
import requests

header = """\

**Lead by**: [nagracks](http://github.com/nagracks)


----------------------------------------------------
Thanks to the following people for their contributions
----------------------------------------------------

"""
url = "https://api.github.com/repos/nagracks/reddit_get_top_images/contributors"

r = requests.get(url)
contributors = r.json()

lines = []
for i in contributors:
    url = (i.get('html_url'))
    username = i.get('login')
    lines.append('* [{}]({}) '.format(username, url))

text = header + '\n'.join(lines)

with open('AUTHORS.md', 'w') as f:
    f.write(text)
