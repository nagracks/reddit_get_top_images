#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reddit Get Top Images
It is a Python script which allows you to download top images from 
any subreddit. 

It allows you to download top pics by categories
top_from_hour
top_from_day
top_from_week
top_from_month
top_from_year
top_from_all
"""

__author__    = "nagracks"
__date__      = "18-07-2016"
__license__   = "GPL3"
__copyright__ = "Copyright © 2016 nagracks"

import argparse
import os

# External modules
import praw
import requests
import tqdm
from bs4 import BeautifulSoup


class TopImageRetreiver(object):

    """TopImageRetreiver Class

    Constructor args:
    :subreddit: subreddit name
    :limit: max limit of getting urls, default set to 15

    method:
    * get_top_submissions

    """

    def __init__(self, subreddit, limit=15):
        # praw Python Reddit API wrapper
        r = praw.Reddit(user_agent="Get top images")
        # subreddit object
        self.submissions = r.get_subreddit(subreddit)
        # Maximum URL limit
        self.limit = limit
        # self.period = period
        self.timeframe = {'h': 'get_top_from_hour',
                          'd': 'get_top_from_day',
                          'w': 'get_top_from_week',
                          'm': 'get_top_from_month',
                          'y': 'get_top_from_year',
                          'a': 'get_top_from_all'}

    def get_top_submissions(self, period):
        """
        Get top images by the selected period.
        :period: string, key for self.timeframe dict
        :return: generator, urls
        """
        # take first lower letter of a period
        # if letter not in the self.timeframe, gets top from the week
        time_period = self.timeframe.get(period[0].lower(), 'get_top_from_week')
        get_top = getattr(self.submissions, time_period)(limit=self.limit)
        return _yield_urls(get_top)


def _yield_urls(submissions):
    """Generate image urls with various url conditions

    :submissions: iterable, subreddit submissions
    :returns: generator, urls
    """
    for submission in submissions:
        url = submission.url
        # Need image extensions
        img_ext = ('jpg', 'jpeg', 'png', 'gif')
        # Url conditions
        # If URL simply ends with needed extension
        # then generate it
        if url.endswith(img_ext):
            yield url
        # If URL contain '/gallery/' or '/a/'
        # Call function made to extract images from it
        elif 'imgur' in url and ('/a/' in url or '/gallery/' in url):
            for link in links_from_imgur(url):
                yield link
        # If url without extension
        else:
            # Make raw url, with incorrect extension.
            raw_url = url + '.jpg'
            # Raw response object
            r = requests.get(raw_url)
            # Get correct extension
            extension = r.headers['content-type'].split('/')[-1]
            # If it is the extension we need
            # Make link
            if extension in img_ext:
                link = "{url}.{ext}".format(url=url, ext=extension)
                yield link


def links_from_imgur(url):
    """Get links from imgur.com/a/ and imgur.com/gallery/

    :url: url contain 'imgur.com/a/' or 'imgur.com/gallery/'
    :returns: generator, links
    """
    # Response object
    r = requests.get(url).text
    # Soup object
    soup_ob = BeautifulSoup(r, 'html.parser')
    # Get image links
    if '/a/' in url or '/gallery/' in url:
        for link in soup_ob.find_all('div', {'class': 'post-image'}):
            try:
                img_link = link.img.get('src')
                # img_link comes as //imgur.com/id
                # Make it https://imgur.com/id
                full_link = 'https:' + img_link
                yield full_link
            except:
                pass

def make_path(filename, dst=''):
    """Make download path

    :filename: name of file which ends the path
    :dst: destination path, default to ''
    :returns: path, full filename path
    """
    # Get home directory
    home_dir = os.path.expanduser('~')
    # Make download directory path
    if dst:
        path = dst
    else:
        path = os.path.join(home_dir, 'reddit_pics')
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except OSError as e:
                print(e)

    # Full file save path
    save_path = os.path.join(path, filename)
    return save_path

def download_it(url):
    """Download the url

    :url: downloadable url address
    :subreddit_name
    """
    # Splits to get some characters from in-url filename
    # This helps to make random filename
    url_chars = url.split('/')[-1][-10:]
    # Make random filename with subreddit name and random chars
    file_name = "{name}_{chars}".format(name=args.subreddit, chars=url_chars)
    # Make save math with condition
    # If user specified path or not
    if args.dst:
        save_path = make_path(file_name, args.dst)
    else:
        save_path = make_path(file_name)

    if os.path.exists(save_path):
        print("{file_name} already downloaded".format(file_name=file_name))
    else:
        print("Downloading to {save_path}".format(save_path=save_path))
        # Response object
        r = requests.get(url, stream=True)
        # Start download
        # Shows progress bar
        with open(save_path, 'wb') as f:
            for chunk in (tqdm.tqdm(r.iter_content(chunk_size=1024),
                         total=(int(r.headers.get('content-length', 0))//1024),
                         unit='KB')):
                if chunk:
                    f.write(chunk)
                else:
                    return


def parse_args():
    """Parse args with argparse
    :returns: args
    """
    parser = argparse.ArgumentParser(description="Download top pics from "
                                                 "any subreddit")

    parser.add_argument('--destination', '-d',
                        dest='dst',
                        action='store',
                        help="Destiantion path")
    
    parser.add_argument('--subreddit', '-s',
                        dest='subreddit',
                        action='store',
                        required=True,
                        help="Name of the subreddit")
    parser.add_argument('--period', '-p',
                        dest='period',
                        action='store',
                        required=True,
                        help="Period of time from which you want images:\n"
                             "[h]our, [d]ay, [m]onth, [y]ear, or [a]ll")
    parser.add_argument('--limit', '-l',
                        dest='limit',
                        type=int,
                        action='store',
                        help="Maximum URL limit")

    return parser.parse_args()


if __name__ == "__main__":
    # Commandline args
    args = parse_args()

    # Args conditions
    # Initialise object
    if args.limit:
        tir = TopImageRetreiver(args.subreddit, args.limit)
    else:
        tir = TopImageRetreiver(args.subreddit)

    for url in tir.get_top_submissions(args.period):
        download_it(url)
