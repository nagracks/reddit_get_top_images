#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__    = "nagracks"
__date__      = "18-07-2016"
__license__   = "MIT"
__copyright__ = "Copyright © 2016 nagracks"

import argparse
import json
import os
import sys

import praw
import requests
import tqdm
from bs4 import BeautifulSoup


def get_top_submissions(subreddit, limit, period):
    """Get top submissions from selection time period with limit

    Parameters
    ----------
    subreddit : str
        Name of the subreddit
    limit : int
        Max limit of getting submissions
    period : str
        A single character. Possible values are `[h]our`, `[d]ay`,
        `[w]eek`, `[m]onth`, `[y]ear` and `[a]ll`.

    Yields
    -------
    str
        Subreddit submissions

    Examples
    --------
    ::

        for submission in get_top_submissions('getmotivated', 15, 'h'):
            # This is submission title
            print(submission)
            # This is submission url
            print(submission.url)
    """
    r = praw.Reddit(user_agent='nagracks')
    all_submissions = r.get_subreddit(subreddit, fetch=True)
    timeframe = {
            'h': all_submissions.get_top_from_hour,
            'd': all_submissions.get_top_from_day,
            'w': all_submissions.get_top_from_week,
            'm': all_submissions.get_top_from_month,
            'y': all_submissions.get_top_from_year,
            'a': all_submissions.get_top_from_all
            }
    return timeframe.get(period)(limit=limit)


def image_urls(submissions):
    """Provides downloadable image urls. This works like this, if url
    simply ends with image extensions then it will yield it otherwise it
    will go on with other conditions. Other conditions are if url
    contain ``imgur`` and ``/a`` or ``/gallery/`` then it will yield
    urls with the help of ``BeautifulSoup``. And at the last if none of
    these two methods works it will try to get downloadable image url by
    making raw url by adding `.jpg` at the end of url and then checks
    its headers' content-type if it is compatible image then generate
    that url.

    Parameters
    ----------
    submissions : generator
        Subreddit submissions

    Yields
    -------
    str
        Downloadable image urls

    Examples
    --------
    ::

        submissions = get_top_submissions(
                        subreddit, args.limit, args.period
                        )
        for image_url in image_urls(submissions):
            # Downloadble image url
            print(image_url)
    """
    for submission in submissions:
        url = submission.url
        img_ext = ('jpg', 'jpeg', 'png', 'gif')
        if url.endswith(img_ext):
            yield url
        elif 'imgur' in url and ('/a/' in url or '/gallery/' in url):
            r = requests.get(url).text
            soup_ob = BeautifulSoup(r, 'html.parser')
            for link in soup_ob.find_all('div', {'class': 'post-image'}):
                try:
                    partial_url = link.img.get('src')
                    # img_link comes as //imgur.com/id make it
                    # https://imgur.com/id
                    url = 'https:' + partial_url
                    yield url
                except:
                    pass
        else:
            raw_url = url + '.jpg'
            try:
                r = requests.get(raw_url)
                r.raise_for_status()
                extension = r.headers['content-type'].split('/')[-1]
            except Exception as e:
                extension = ''
            if extension in img_ext:
                link = '{url}.{ext}'.format(url=url, ext=extension)
                yield link


def download_images(url, subreddit_name, destination):
    """Download images

    Parameters
    ----------
    url : str
        Image url to download
    subreddit_name : str
        Subreddit name
    destination : str
        Destination path to save image

    Returns
    -------
        Write data to file
    """
    # `?` and `&` should not present in filename so replace them with
    # `X`
    table = str.maketrans('?&', 'XX')
    # Splits url to get last 10 `characters` from `in-url filename`
    # This helps to make random filename by joining `subreddit` name and
    # `in-url` filename characters
    url_chars = (url.split('/')[-1][-10:]).translate(table)
    # Make filename
    filename = "{name}_{chars}".format(name=subreddit_name, chars=url_chars)
    # Make full path to save destination of images
    if destination:
        path = os.path.expanduser(destination)
    else:
        path = os.path.expanduser('~')
        path = os.path.join(path, 'reddit_pics')
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    if os.path.exists(file_path):
        print("{} is already downloaded".format(filename))
    else:
        print("Download to {}".format(file_path))
        r = requests.get(url, stream=True)
        with open(file_path, 'wb') as outfile:
            for chunk in (
                    tqdm.tqdm(r.iter_content(chunk_size=1024),
                    total=(int(r.headers.get('content-length', 0)) // 1024),
                    unit='KB')
                    ):
                if chunk:
                    outfile.write(chunk)
                else:
                    return


class ArgumentConfig(object):

    """ArgumentConfig class

    Parameters
    ----------
    parser: argparse.ArgumentParser
        All the arguments

    Methods
    -------
    parse_args
    """
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser
        self.parser.add_argument(
                '--config', '-c',
                nargs='?',
                const='stdout',
                help= """
                    Read arguments from config file. The config can be
                    generated with --write-config option
                """
                )
        self.parser.add_argument(
                '--write-config', '-wc',
                nargs='?',
                metavar='FILENAME',
                const='stdout',
                help= """
                    Print script options to screen in JSON format and if
                    FILENAME is specified then write to that file
                """
                )

    def parse_args(self, *args, **kwargs):
        """Parse commandline args args

        Parameters
        ----------
        *args
        **kwargs

        Returns
        -------
            Argparse namespace
        """
        # Parse an empty list to get the defaults
        defaults = vars(self.parser.parse_args([]))
        passed_args = vars(self.parser.parse_args(*args, **kwargs))
        # Only keep the args that aren't the default
        passed_args = {
                key: value for (key, value) in passed_args.items()
                if (key in defaults and defaults[key] != value)
                }
        config_path = passed_args.pop('config', None)
        if config_path:
            with open(config_path, 'r') as config_file:
                config_args = json.load(config_file)
        else:
            config_args = dict()

        # Override defaults with config with passed args
        options = {**defaults, **config_args, **passed_args}
        # Remove the config options from options. They're not needed any
        # more and we don't want them serialized
        options.pop('config', None)
        options.pop('write_config', None)

        # Print the options (to file) if needed
        config_dst = passed_args.pop('write_config', None)
        if config_dst:
            print(json.dumps(options, sort_keys=True, indent=4))
            if config_dst != 'stdout':
                with open(config_dst, 'w', encoding='utf-8') as config_file:
                    print(json.dumps(options, sort_keys=True, indent=4), file=config_file)
                    print("Current options saved to: {}".format(config_dst))
            sys.exit(0)

        return argparse.Namespace(**options)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '-s', '--subreddit',
            default=['earthporn', 'cityporn'],
            nargs='+',
            help="""
                Name of the subreddits. Provide as many subreddits you
                want to download images from.
            """
            )
    parser.add_argument(
            '-p', '--period',
            default='w',
            choices=['h', 'd', 'w', 'm', 'y', 'a'],
            help="""
                [h]our, [d]ay, [w]eek, [m]onth, [y]ear, or [a]ll. Period
                of time from which you want images. Default to
                'get_top_from_[w]eek'
            """
            )
    parser.add_argument(
            '-l', '--limit',
            metavar='N',
            type=int,
            default=15,
            help="""
                Maximum URL limit per subreddit. Defaults to 15
            """
            )
    parser.add_argument(
            '--destination', '-d',
            help="""
                Destination path. By default it saves to $HOME/reddit_pics
            """
            )

    argconfig = ArgumentConfig(parser)
    args = vars(argconfig.parse_args())

    # Handle control+c nicely
    import signal
    def exit_(signum, frame):
        os.sys.exit(1)
    signal.signal(signal.SIGINT, exit_)

    # Download images
    for subreddit in args['subreddit']:
        submissions = get_top_submissions(
                        subreddit, args['limit'], args['period']
                        )
        for image_url in image_urls(submissions):
            download_images(image_url, subreddit, args['destination'])
