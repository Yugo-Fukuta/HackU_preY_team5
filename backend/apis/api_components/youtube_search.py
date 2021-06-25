from datetime import datetime, timedelta, timezone
from dateutil import parser
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import isodate

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

class YouTube_Search_Instance:
    def __init__(self, MyAPIKey):
        self.DEVELOPER_KEY = MyAPIKey
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
        ids = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                '''data = dict()
                data["videoId"] = search_result["id"]["videoId"]
                data["publishedAt"] = search_result["snippet"]["publishedAt"]
                data["title"] = search_result["snippet"]["title"]
                data["videoUrl"] = "https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
                data["thumbnailsUrl"] = search_result["snippet"]["thumbnails"]["high"]["url"]
                videos.append(data)'''
                ids.append(search_result["id"]["videoId"])

        res = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=','.join(ids) # カンマ区切りで複数のidを一度に渡せます
        ).execute()

        for vid in res["items"]:
            duration1 = isodate.parse_duration(vid['contentDetails']['duration'])
            duration = int(duration1.total_seconds())
            hour = duration // 3600
            min = (duration-3600*hour) // 60
            sec = duration % 60
            if hour > 0:
                durationHMS = '%i:%i:%i' % (hour, min, sec)
            else:
                durationHMS = '%i:%i' % (min, sec)
            pbat = vid['snippet']['publishedAt']
            jst_time = parser.parse(pbat)
            jst_tz = timezone(timedelta(hours=+9))
            videos.append({
            'title': vid['snippet']['title'],
            'id': vid['id'],
            'videoUrl': 'https://www.youtube.com/watch?v=%s' % vid['id'],
            'thumbnailsUrl': vid["snippet"]["thumbnails"]["high"]["url"],
            'description': vid['snippet']['description'],
            'publishedAt': datetime.fromtimestamp(jst_time.timestamp(), jst_tz).strftime("%Y/%m/%d %H:%M"),
            'duration': durationHMS,
            'viewCount': int(vid['statistics']['viewCount']),
            'likeCount': int(vid['statistics']['likeCount']),
            'dislikeCount': int(vid['statistics']['dislikeCount']),
            })
        return videos

    def get_meta_data(self, videoIDs): # カンマ区切り文字列 videoIDsの例 vOczUoQigww,q4DKmdlUb6I,v0M0Kd5w_fY
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
            developerKey=self.DEVELOPER_KEY)

        search_response = youtube.videos().list(
                part="id,statistics,status",
                id=videoIDs
        ).execute()

        items = search_response.get("items", [])
        meta_data = []

        for item in items:
            data = dict()
            data["videoId"] = item["id"]
            data["statistics"] = item["statistics"]
            meta_data.append(data)

        return meta_data

    if __name__ == "__main__":
        argparser.add_argument("--q", help="Search term", default="Google")
        argparser.add_argument("--max-results", help="Max results", default=25)
        args = argparser.parse_args()

        try:
            youtube_search(args)
        except Exception as e:
            print(e)
        