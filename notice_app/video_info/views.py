from django.shortcuts import render, redirect
from django.views import View

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from atproto import Client, client_utils

import os
import environ
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# .envファイルを読み込む
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))


# トップページ
class IndexView(View):
    def get(self, request):
        return render(request, "video_info/index.html")


# 一覧
class InfoMainView(View):
    # 初期表示
    def get(self, request):

        api = YouTubeApi()
        result = api.get()

        return render(
            request,
            "video_info/info_main.html",
            {"resultVideoInfo": result},
        )


# 送信処理
class InfoSendView(View):
    def post(self, request):

        video_url = request.POST.getlist("video_url")
        video_titles = request.POST.getlist("video_titles")

        BlueskyAlert(video_url[0], video_titles[0]).send()

        return redirect("video_info:info_main")


# YouTube_Apiから動画情報を取得する
class YouTubeApi:
    def get(self):
        # API情報
        DEVELOPER_KEY = env("DEVELOPER_KEY")
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        youtube = build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
        )

        # 任意のチャンネルIDで検索を実行
        search_response = (
            youtube.search()
            .list(
                part="snippet",
                channelId="UC0v-pxTo1XamIDE-f__Ad0Q",
                order="date",
                type="video",
                maxResults=5,
            )
            .execute()
        )

        # データ確認用
        # print(search_response)

        result = {}
        # 検索結果からvideoIdとtitleの値を取得する
        for item in search_response.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            title = item.get("snippet", {}).get("title")

            result[video_id] = title

        return result


# Blueskyに通知を送る
class BlueskyAlert:
    def __init__(self, video_url, video_title):
        self.video_url = video_url
        self.video_title = video_title

    def send(self):
        client = Client()

        USER_ID = env("USER_ID")
        PASSWORD = env("PASSWORD")

        client.login(USER_ID, PASSWORD)

        text_builder = client_utils.TextBuilder()
        text_builder.text("[パテレ更新通知]")
        text_builder.link(self.video_title, self.video_url)

        client.send_post(text_builder)


index = IndexView.as_view()
info_main = InfoMainView.as_view()
info_send = InfoSendView.as_view()
