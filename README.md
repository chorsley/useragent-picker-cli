# UA generator

Generates random but realistic user agents (UAs) on a command line (or via API, if you like).

    $ uagen mobile chrome
    Mozilla/5.0 (Linux; Android 10; TAS-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.64 HuaweiBrowser/10.0.5.300 Mobile Safari/537.36

# Use case

You want to:

* generate realistic-looking user agents with curl, wget, httpie etc
* stop tediously searching for, copying, and pasting user agent strings from long UA lists
* have realistic-looking HTTP requests using common user agent strings via curl and friends
* filter the UAs you choose depending on OS, platform (desktop, mobile, tablet), and browser
* refrain from checking the UA generator doco every single time to see if it's actually `--msie`, `--ie`, or `--iexplore`.

# Installation

If you don't use `pipsi`, you're missing out.
Here are [installation instructions](https://github.com/mitsuhiko/pipsi#readme).

Simply run:

    $ pipsi install ua-gen-cli

# Usage

`uagen` can be used by listing some filter criteria you'd like to use:

    $ uagen chrome macos   # Chrome on MacOS
    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36

    $ uagen chrome osx     # Chrome on MacOS again
    Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36

There are many aliases, so just try what makes sense to you and it will probably work. If not, submit an issue!

If you want something a little niche that's not in the supported keyword list, uagen will search through browser UAs as a fallback:

    $ python3 -mua_gen.cli trident
    ** 'trident' didn't match any known filters, looking for matching browser strings
    Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko

`uagen` simply outputs a single user agent matching your criteria. This can be combined with HTTP agents like this:

    $ curl --user-agent "`uagen`" http://example.com
    $ curl -v --user-agent "uagen nokia mobile`" http://example.com
    ...
    > GET / HTTP/1.1
    > Host: example.com
    > User-Agent: Mozilla/5.0 (Linux; Android 10; Nokia 7 plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.360

You could also alias this for convenience:

    $ alias uacurl='curl --user-agent "`uagen`"
    $ uacurl -v http://example.com
    > GET / HTTP/1.1
    > Host: example.com
    > User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36

Since `uagen` respects weightings based on usage in the wild, if you ran it 1000 times, you'd get a rough % breakdown of UAs
like actual usage.

## Programatic usage

`ua-gen-cli` is primarily designed for CLI use, but you can use it programatically too if you'd like:

```
from ua_gen.cli import UAGen
ua = UAGen()
print(ua.get_ua(["mobile"]))
print(ua.get_ua(["firefox", "desktop"]))
```

## Data source

The user agent data file used lives at `$HOME/.ua_cli_gen/enriched_ua_db.json`, so feel free to have a look.

## Acknowledgements

This project was inspired by and relies on data from https://github.com/intoli/user-agents.

