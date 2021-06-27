from oauth2client.tools import argparser
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
        return data

    def twitter_user_search(self, q, maxResults=5):
        twitter = Twitter(
            auth=OAuth(self.access_token, self.access_token_secret,
                       self.api_key, self.api_key_secret)
        )
        data = twitter.users.search(q=q, lang="ja", count=maxResults)
        return data


    if __name__ == "__main__":
        argparser.add_argument("--q", help="Search term", default="Google")
        argparser.add_argument("--max-results", help="Max results", default=25)
        args = argparser.parse_args()

        try:
            twitter_search(args)
        except Exception as e:
            print(e)
