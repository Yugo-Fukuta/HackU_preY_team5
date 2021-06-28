import argparse
from twitter import *

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

class Twitter_Search_Instance:
    def __init__(self, auth_info):
        self.api_key = auth_info.api_key
        self.api_key_secret = auth_info.api_key_secret
        self.access_token = auth_info.access_token
        self.access_token_secret = auth_info.access_token_secret

    def twitter_search(self, q, maxResults=25):
        twitter = Twitter(auth=OAuth(self.access_token, self.access_token_secret, 
            self.api_key, self.api_key_secret))

        data = twitter.search.tweets(q=q, lang='ja', result_type='popular', count=maxResults)
        tweets_data = data["statuses"]

        # URL処理
        for i, tw in enumerate(tweets_data):
            urls = tw["entities"].get("urls")
            media = tw["entities"].get("media")
            tweets_data[i]["extracted_urls"] = []

            if urls:
                for u in urls:
                    tweets_data[i]["extracted_urls"].append(u["expanded_url"])
                    tweets_data[i]["text"] = \
                        tweets_data[i]["text"].replace(f"{u['url']}\n", "")\
                                              .replace(u["url"], "")

            if media:
                for m in media:
                    tweets_data[i]["extracted_urls"].append(m["media_url"])
                    tweets_data[i]["text"] = \
                        tweets_data[i]["text"].replace(f"{m['url']}\n", "")\
                                              .replace(m["url"], "")

            tweets_data[i]["text"] = tweets_data[i]["text"].strip()

        return tweets_data

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    argparser.add_argument("--api-key", required=True)
    argparser.add_argument("--api-key-secret", required=True)
    argparser.add_argument("--access-token", required=True)
    argparser.add_argument("--access-token-secret", required=True)
    args = argparser.parse_args()

    try:
        t = Twitter_Search_Instance(args)
        t.twitter_search(args.q, args.max_results)
    except Exception as e:
        print(e)
