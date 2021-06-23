from oauth2client.tools import argparser
import requests

class News_Search_Instance:
    def __init__(self, MyAPIKey):
        self.MyAPIKey = MyAPIKey

    def news_search(self, q):
        url = 'https://newsapi.org/v2/everything?q={}&apiKey={}&sortBy=popularity'.format(q, self.MyAPIKey)
        response = requests.get(url)
        response = response.json()
        return response

    if __name__ == "__main__":
        argparser.add_argument("--q", help="Search term", default="Google")
        args = argparser.parse_args()

        try:
            news_search(args)
        except Exception as e:
            print(e)
