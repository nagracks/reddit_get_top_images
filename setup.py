#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup


with open('requirements.txt') as infile:
    requirements = infile.read()


setup(
    version='v0.1.0',
    name='reddit_get_top_images',
    description='Download top images from any subreddit',
    licence='MIT',

    author='nagracks',
    author_email='nagracks@gmail.com',

    url='https://github.com/nagracks/reddit_get_top_images',
    download_url='https://github.com/nagracks/reddit_get_top_images/archive/v0.1.0.tar.gz',

    keywords='reddit script download top images',

    scripts=['get_top_images.py'],
    install_requires=requirements,
)
