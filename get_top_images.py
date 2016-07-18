#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = "nagracks"
__date__      = "18-07-2016"
__license__   = "MIT"
__copyright__ = "Copyright © 2016 nagracks"

import os

# External modules #
import praw
import requests

def get_top_images(subreddit):
    """Get top images of day from subreddit

    :subreddit: subreddit name, eg. getmotivated
    :returns: generator, url
    """
    # praw Python Reddit API wrapper #
    r = praw.Reddit('Download top pics of Day from '
                    '{subreddit}.reddit.com'.format(subreddit=subreddit))
    # subreddit object #
    submissions = r.get_subreddit('getmotivated').get_top_from_day()

    # Get image links #
    for submission in submissions:
        url = submission.url
        if url.endswith(('jpg', 'png', 'jpeg')):
            yield url

def download_it(url):
    """Download the url

    :url: downloadable url address
    """
    # Splits to get some characters from in-url filename #
    # Helps to make random filename #
    url_chars = url.split('/')[-1][-10:]
    # Make random filename #
    file_name = 'get_motivated_{chars}'.format(chars=url_chars)

    # Get home directory #
    home_dir = os.path.expanduser('~')
    # Make download path #
    path = os.path.join(home_dir, 'get_motivated_pics')
    if os.path.exists(path):
        pass
    else:
        try:
            os.mkdir(path)
        except OSError as e:
            print(e)

    # File save path #
    save_path = os.path.join(path, file_name)

    if os.path.exists(save_path):
        print ("{file_name} already downloaded".format(file_name=file_name))
    else:
        print ("Downloading to {save_path}".format(save_path=save_path))
        # Start download #
        r = requests.get(url, stream=True)
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

if __name__ == "__main__":
    # Get top images #
    for img_url in get_top_images('getmotivated'):
        download_it(img_url)
