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
for url in tir.get_top_submissions('w'):
    gi.download_it(url, sub_reddit)
```

**Here is a typical CLI usecase that will do the same:**

`python get_top_images.py -s getmotivated --week`

**Here are the full arguments for CLI use:**

```
usage: get_top_images.py [-h] --subreddit SUBREDDIT --period PERIOD
                         [--limit LIMIT]

Download top pics from any subreddit

optional arguments:
  -h, --help            show this help message and exit
  --subreddit SUBREDDIT, -s SUBREDDIT
                        Name of the subreddit
  --period PERIOD, -p PERIOD
                        Period of time from which you want images: [h]our,
                        [d]ay, [m]onth, [y]ear, or [a]ll
  --limit LIMIT, -l LIMIT
                        Maximum URL limit
```

Contributing
------------

This project is intended as a beginner friendly collaborative code, and anyone that wants to add, extend or otherwise improve this code is free to do so. Even if they have never contributed to another repository before.

LICENSE
------

`reddit_get_top_images` is licensed under
[GPL3](LICENSE)
