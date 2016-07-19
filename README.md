# reddit_get_top_images

> `reddit_get_top_images` is script used to download top images 
> from any subreddit.

Usage
-----

```
usage: get_top_images.py [-h] --subreddit SUBREDDIT [--limit LIMIT] [--hour]
                         [--day] [--week] [--month] [--year] [--all]

Download top pics from any subreddit

optional arguments:
  -h, --help            show this help message and exit
  --subreddit SUBREDDIT, -s SUBREDDIT
                        Name of the subreddit
  --limit LIMIT, -l LIMIT
                        maximum limit of getting images
  --hour, -1            Get top images from *hour*
  --day, -d             Get top images from *day*
  --week, -w            Get top images from *week*
  --month, -m           Get top images from *month*
  --year, -y            Get top images from *year*
  --all, -a             Get top images from *all*
```

**Download `top images from day` from any `subreddit` like this**

`$python get_top_images.py -s getmotivated --day`

`$python get_top_images.py -s getmotivated --all --limit 500`

Contributing
------------

Feel free to improve `reddit_get_top_images`. All kind of pull-requests are welcome.

LICENSE
------

`reddit_get_top_images` is licensed under 
[MIT](LICENSE)
