# -*- coding: utf-8 -*-

import os
import pickle
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

def main(title, description, videoPath, thumbnailPath):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    CLIENT_SECRET_FILE = "" #Youtube Data Api Client Secret file goes here
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    
    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=cred)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": "24",
            "description": description,
            "title": title,
            "tags" : ["ask reddit stories","askreddit","askreddit best posts","askreddit best questions","askreddit funny","askreddit scary","askreddit stories","askreddit top posts","askreddit top questions","best of askreddit","best of reddit","best reddit posts","cowbelly","dank memes","dankmemes","memes","r/askreddit","radio","radio tts","reddit","reddit best posts","reddit jar","reddit memes","reddit post video","reddit scary","reddit stories","reddit top posts","redditors","top posts","updoot","wholesome","wholesome memes"]
          },
          "status": {
            "privacyStatus": "public",
            'selfDeclaredMadeForKids': False
          },
          'notifySubscribers': True
        },
    
        media_body=MediaFileUpload(videoPath, resumable=True)
    )
    response_upload = request.execute()
    print(response_upload)

    request = youtube.thumbnails().set(
        videoId=response_upload.get('id'),
        
        media_body=MediaFileUpload(thumbnailPath)
    )
    response = request.execute()
    print(response)
