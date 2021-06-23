from datetime import datetime, timedelta
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

class YouTube_Search_Instance:
    def __init__(self, MyAPIKey):
        self.MyAPIKey = MyAPIKey
        #DEVELOPER_KEY = "YOUR_YOUTUBE_API_KEY"
        self.DEVELOPER_KEY = self.MyAPIKey
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

    def youtube_search(self, q, maxResults=10):
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
            developerKey=self.DEVELOPER_KEY)

        # Call the search.list method to retrieve results matching the specified
        # query term.
        one_week_ago = (datetime.today() - timedelta(days=7))
        one_week_ago_iso = one_week_ago.isoformat("T") + "Z"

        search_response = youtube.search().list(
            q=q,
            part="id,snippet",
            maxResults=maxResults,
            type="video",
            publishedAfter=one_week_ago_iso,
            safeSearch="strict",
            regionCode="JP"
        ).execute()

        videos = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append("title: %s, videoUrl: https://www.youtube.com/watch?v=%s thumbnailsUrl: %s" 
                        % (search_result["snippet"]["title"], search_result["id"]["videoId"], search_result["snippet"]["thumbnails"]["high"]["url"]))

        #print("Videos:\n", "\n".join(videos), "\n")
        return videos

    if __name__ == "__main__":
        argparser.add_argument("--q", help="Search term", default="Google")
        argparser.add_argument("--max-results", help="Max results", default=25)
        args = argparser.parse_args()

        try:
            youtube_search(args)
        except Exception as e:
            print(e)
