# reddit_get_top_images

> `reddit_get_top_images` is a script that can be used to download
> all the top images from any subreddit of http://www.reddit.com.

> It can be adjusted to get images from any segment of time,
> like images from the last hour, day, or week etc.

> The script will create a folder in your $home directory
> called `reddit_pics`.

Usage
-----

**Here is a typical API usecase that will get all the top images**
**of www.reddit.com/r/getmotived from last week.**
```
import get_top_images as gi

sub_reddit = 'getmotivated'
tir = gi.TopImageRetreiver(sub_reddit, limit=5)
for url in tir.get_from_week():
    gi.download_it(url, sub_reddit)
```

**Here is a typical CLI usecase that will do the same:**

`python get_top_images.py -s getmotivated --week`

**Here are the full arguments for CLI use:**

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

Contributing
------------

This project is intended as a beginner friendly collaborative code, and anyone that wants to add, extend or otherwise improve this code is free to do so. Even if they have never contributed to another repository before.

LICENSE
------

`reddit_get_top_images` is licensed under
[GPL3](LICENSE)
