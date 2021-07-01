import argparse
from typing import Optional
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
        self._extract_urls(tweets_data)

        return tweets_data

    def twitter_user_search(self, q, maxResults=5,
                            include_rts=False, include_replies=False):
        twitter = Twitter(
            auth=OAuth(self.access_token, self.access_token_secret,
                       self.api_key, self.api_key_secret)
        )
        data = twitter.users.search(q=q, lang="ja", count=5)

        # 公式マークがないなら空のリスト
        if not data[0]["verified"]:
            return []

        usrid = data[0]["id_str"]

        res = twitter.statuses.user_timeline(
            _id=usrid,
            count=maxResults,
            include_rts=include_rts,
            exclude_replies=not include_replies)
        self._extract_urls(res)
        return res

    def _extract_urls(self, statuses):
        """Given a list of statuses, remove all URLs from `text`
        and store them in `extracted_urls`.
        """
        for i, tw in enumerate(statuses):
            urls = tw["entities"].get("urls")
            media = tw["entities"].get("media")
            statuses[i]["extracted_urls"] = []

            if urls:
                for u in urls:
                    statuses[i]["extracted_urls"].append(u["expanded_url"])
                    statuses[i]["text"] = \
                        statuses[i]["text"].replace(f"\n{u['url']}\n", "")\
                                           .replace(u["url"], "")

            if media:
                for m in media:
                    statuses[i]["extracted_urls"].append(m["media_url"])
                    statuses[i]["text"] = \
                        statuses[i]["text"].replace(f"\n{m['url']}\n", "")\
                                           .replace(m["url"], "")

            statuses[i]["text"] = statuses[i]["text"].strip()

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
        # t.twitter_search(args.q, args.max_results)
        print(t.twitter_user_search(args.q, args.max_results))
    except Exception as e:
        print(e)
