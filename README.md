# RT-queue-for-twitter

[![py](https://github.com/Charlignon/RT-queue-for-twitter/actions/workflows/scheduledRT.yml/badge.svg)](https://github.com/Charlignon/RT-queue-for-twitter/actions/workflows/scheduledRT.yml)

This app was made to recreate on Twitter the queue system from Tumblr, which allow you to reblog/RT posts automatically at a set frequency. It was created for the sake of the [@VoloStan](https://twitter.com/VoloStan) account on Twitter.
I cannot use this app anymore for several reasons :
- Twitter's Free plan was effectively put to an end, as we can only post and not retreive tweets now
- The Basic plan is way to expensive for such a small scale project (I'm not paying $100 to post <750 tweets per month)
- Twitter api V1.1 as been deprecated forever. I was heavily leveraging the Collection feature, but V2 does not provide any way to access this data
- Tweetdeck (the only tool available to manage Collections) will probably be terminated sooner or later
I intended to clean and refacto the code before open-sourcing it, but since I won't invest any more time on this I am releasing the code "as it". I hope you will find it interesting, and sorry for the bad code quality it's just a PoC :)

# How it would have worked

This app is leveraging several tools to perform its tasks :
- The Collection feature from Twitter, which is basically an arbitrary set of tweets
- TweetDeck, the only official Twitter service that let you create and edit Collections
- Periodically ran Github Actions, which prevent the need for running a bot on a server

## Setup
- Fork this project (make it private to protect your tokens)
- Login on [Tweetdeck](tweetdeck.twitter.com/) with [BetterTweetDeck](https://better.tw/) installed and switch to the legacy interface
- Create a new Collection, open it on Twitter and copy the id from the URL
- Assuming you already have a Twitter developer account and an project with Elevated access, go in you project settings and copy your keys and tokens
- Fill in the blanks in the Python file
- Download the repo, edit the python file to call only the `get_access_token()` method and run it. Fill in the blanks in your repo

## Tweaking the settings
- In the Python file, you can adjust how many tweets are RT at once
- In the .github/workflows/scheduledRT.yml file, you can set the RT frequency by changing the cron. Be mindful of Github's rate limiting on Actions
