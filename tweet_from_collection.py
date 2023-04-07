import tweepy
from TwitterAPI import TwitterAPI

## Init
consumer_key="<YOUR KEY HERE>"
consumer_secret="<YOUR SECRET HERE>"
access_token="<ACCESS_TOKEN HERE>"
access_token_secret="<ACCESS_TOKEN SECRET HERE>"


user_id="1471162491631714308" # VoloStan
collection_id="custom-<THE COLLECTION ID>"
route = "collections/entries"

HOW_MANY = 1 # How many entries you want to RT at once

client_v1 = TwitterAPI(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
client_v2 = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)


## Methods

# Call this only once to initialise your access token
def get_access_token():
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret,
        callback="oob"
    )
    print(oauth1_user_handler.get_authorization_url())

    verifier = input("Input PIN: ")
    access_token, access_token_secret = oauth1_user_handler.get_access_token(
        verifier
    )
    print(access_token, access_token_secret)


def get_all_tweets_from_collection():
    tweet_array = []
    counter = 0
    last_tweet_id = 0
    while True:
        params = {'id':collection_id, 'count':'200', 'max_position':last_tweet_id} if last_tweet_id>0 else  {'id':collection_id, 'count':'200'}
        next_tweet_array = client_v1.request(route, params).json()["response"]["timeline"]
        counter += len(next_tweet_array)
        if len(next_tweet_array) == 0:
            print("Found " + str(counter) + " tweets in collection.")
            return tweet_array
        previous = last_tweet_id
        tweet_array.extend(next_tweet_array)
        last_tweet_id = int(tweet_array[-1]["tweet"]["sort_index"])

def get_first_tweet_from_collection(collection_id):
    first_tweet_array = client_v1.request(route, {'id':collection_id, 'count':'10'}).json()["response"]["timeline"]
    if len(first_tweet_array) == 0:
        raise SystemExit("Queue is empty !")
    tweet_id = first_tweet_array[0]["tweet"]["id"]
    print("Found tweet with id", tweet_id)
    return tweet_id

def retweet(twwet_id):
    res = client_v2.retweet(tweet_id=twwet_id)
    if not res.data["retweeted"]:
        error_string = ', '.join(str(err) for err in res.errors) 
        raise SystemExit("Error while retweeting : " + error_string)
    print("Retweet successful")


def remove_from_collection(collection_id, tweet_id):
    res = client_v1.request(route + "/remove", {'id':collection_id, 'tweet_id':tweet_id}).json()
    errors = res["response"]["errors"]
    if len(errors) != 0 :
        error_string = ', '.join(str(err) for err in errors) 
        raise SystemExit("Error while removing tweet from collection : " + error_string)
    print("Tweet removed from collection")


def unpile():
    tweet_id = get_first_tweet_from_collection(collection_id)
    retweet(tweet_id)
    remove_from_collection(collection_id, tweet_id)

def unqueue_from(queue):
    isError = False
    tweet_id = queue.pop(-1)["tweet"]["id"]
    print("Retweeting " + tweet_id)
    try:
        retweet(tweet_id)
    except Exception as e :
        isError = True
        print('--------------- ' + tweet_id + ' ------------------')
        print(e)
        print('------------------------------------------------------')
        if (str(e).__contains__('429')):
            raise SystemExit("Too many requests.")
    if (not isError):
        remove_from_collection(collection_id, tweet_id)
    
## Execution
queue = get_all_tweets_from_collection()
limit = min(HOW_MANY, len(queue))
for i in range(limit) :
    print("--- Run #", i+1, "/", limit, " ---", sep="")
    #unpile()
    unqueue_from(queue)
