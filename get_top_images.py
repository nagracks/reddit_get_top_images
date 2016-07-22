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

    methods:
    * get_from_hour
    * get_from_day
    * get_from_week
    * get_from_month
    * get_from_year
    * get_from_all

    """

    def __init__(self, subreddit, limit=15):
        # praw Python Reddit API wrapper
        r = praw.Reddit(user_agent="Get top images")
        # subreddit object
        self.submissions = r.get_subreddit(subreddit)
        # Maximum URL limit
        self.limit = limit

    def get_from_hour(self):
        """Get top images by hour
        :returns: generator, urls
        """
        # Get top from hour
        # Generator object
        get_from_hour = self.submissions.get_top_from_hour(limit=self.limit)
        # Get image links
        return _yield_urls(get_from_hour)

    def get_from_day(self):
        """Get top images by day
        :returns: generator, urls
        """
        # Get top from day
        # Generator object
        get_from_day = self.submissions.get_top_from_day(limit=self.limit)
        # Get image links
        return _yield_urls(get_from_day)

    def get_from_week(self):
        """Get top images by week
        :returns: generator, urls
        """
        # Get top from week
        # Generator object
        get_from_week = self.submissions.get_top_from_week(limit=self.limit)
        # Get image links
        return _yield_urls(get_from_week)

    def get_from_month(self):
        """Get top images by month
        :returns: generator, urls
        """
        # Get top from month
        # Generator object
        get_from_month = self.submissions.get_top_from_month(limit=self.limit)
        # Get image links
        return _yield_urls(get_from_month)

    def get_from_year(self):
        """Get top images by year
        :returns: generator, urls
        """
        # Get top from year
        # Generator object
        get_from_year = self.submissions.get_top_from_year(limit=self.limit)
        # Get image links
        return _yield_urls(get_from_year)

    def get_from_all(self):
        """Get top images by all
        :returns: generator, urls
        """
        # Get top from all
        # Generator object
        get_from_all = self.submissions.get_top_from_all(limit=self.limit)
        # Get image links
        return _yield_urls(get_from_all)


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


def download_it(url, subreddit_name):
    """Download the url

    :url: downloadable url address
    :subreddit_name
    """
    # Splits to get some characters from in-url filename
    # This helps to make random filename
    url_chars = url.split('/')[-1][-10:]
    # Make random filename with subreddit name and random chars
    file_name = "{reddit_name}_{chars}".format(reddit_name=subreddit_name,
                                               chars=url_chars)
    # Get home directory
    home_dir = os.path.expanduser('~')
    # Make download path
    path = os.path.join(home_dir, 'reddit_pics')
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError as e:
            print(e)

    # File save path
    save_path = os.path.join(path, file_name)

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
    # Optional args
    parser.add_argument('--subreddit', '-s',
                        dest='subreddit',
                        action='store',
                        required=True,
                        help="Name of the subreddit")
    parser.add_argument('--limit', '-l',
                        dest='limit',
                        type=int,
                        action='store',
                        help="Maximum URL limit")
    
    # Boolean args
    parser.add_argument('--hour', '-1',
                        dest='hour',
                        action='store_true',
                        help="Get top images from *hour*")
    parser.add_argument('--day','-d',
                        dest='day',
                        action='store_true',
                        help="Get top images from *day*")
    parser.add_argument('--week', '-w',
                        dest='week',
                        action='store_true',
                        help="Get top images from *week*")
    parser.add_argument('--month', '-m',
                        dest='month',
                        action='store_true',
                        help="Get top images from *month*")
    parser.add_argument('--year', '-y',
                        dest='year',
                        action='store_true',
                        help="Get top images from *year*")
    parser.add_argument('--all', '-a',
                        dest='all',
                        action='store_true',
                        help="Get top images from *all*")
    
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

    # If args.name true then download
    if args.hour:
        for url in tir.get_from_hour():
            download_it(url, args.subreddit)
    elif args.day:
        for url in tir.get_from_day():
            download_it(url, args.subreddit)
    elif args.week:
        for url in tir.get_from_week():
            download_it(url, args.subreddit)
    elif args.month:
        for url in tir.get_from_month():
            download_it(url, args.subreddit)
    elif args.year:
        for url in tir.get_from_year():
            download_it(url, args.subreddit)
    elif args.all:
        for url in tir.get_from_all():
            download_it(url, args.subreddit)
