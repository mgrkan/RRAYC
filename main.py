from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS, RESOURCES, BASE_DIR, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT, CREDENTIALS, VIDEOS_DIR
import sys
import shutil
from mutagen.wave import WAVE
from mail_notifier import sendMail, SendMailAttached
import video_creator
import screenshotter
import os
import pathlib
from google.cloud import texttospeech as tts
from moviepy.editor import VideoFileClip
import praw
import youtubeDataApiSample
from thumbnail_creator import createThumb
from clear import folder_preparation, mid_folder_preparation
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS #GCLOUD CREDENTIALS FOR TTS API

upImage = pathlib.Path(RESOURCES + "/images/upvoteIcon.png")
downImage = pathlib.Path(RESOURCES + "/images/downvoteIcon.png")
subIcon = pathlib.Path(RESOURCES + "/images/subIcon.png")
bar = pathlib.Path(RESOURCES + "/images/bar.png")

def text_to_wav(voice_name, text, filename):
    language_code = '-'.join(voice_name.split('-')[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name)
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16,
        speaking_rate=1.080)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config, )

    file = pathlib.Path(SAMPLE_INPUTS + "/audio/" + filename + ".wav")
    with open(file, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{file}"')

reddit = praw.Reddit(client_id = CLIENT_ID,
                     client_secret = CLIENT_SECRET,
                     username = USERNAME,
                     password = PASSWORD,
                     user_agent = USER_AGENT)

def_time = 1080.30  #DEFAULT LENGTH OF THE VIDEOS. 
sub_input = "askreddit"
sub = reddit.subreddit(sub_input)
sub_hot = sub.hot(limit=10)
commentLimit = 83

folder_preparation()

for post in sub_hot:
    
    mid_folder_preparation()

    if post.over_18: #IF POST IS NSFW CONTINUES TO THE NEXT POST
        continue

    if post.stickied: #IF POST IS PINNED CONTINUES TO THE NEXT POST
        continue

    post_title = (post.title).replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u201c", "'").replace(u"\u201d", "'").replace(u"\u2014", "-")

    print("started new video, {} id: {}". format(post_title, post.id))
    try:
        sendMail("Started new video", "Started new video, {} id: {}".format(post_title, post.id))
    except:
        pass
    submission_id = post.id
    vidname = post.id
    submission = reddit.submission(submission_id)
    text_to_wav("en-US-Wavenet-B", submission.title, "1post")  
    print(" - post text converted to wav - ")
    screenshotter.createPostSS(submission.title, sub_input, subIcon, upImage, downImage, str(
        submission.ups), submission.author)
    print(" - created post ss - ")
    imgdir = pathlib.Path(SAMPLE_INPUTS + '/imgs/1post')
    path = os.path.join(SAMPLE_INPUTS, "audio")
    file = os.path.join(path, "1post.wav")
    aud = WAVE(file)
    audio_info = aud.info
    duration = int(audio_info.length)
    output_video = os.path.join(SAMPLE_OUTPUTS, "1post_output.mp4")
    video_creator.makeVideo(imgdir, file, output_video, duration)
    submissionList = []
    submission.comments.replace_more(limit=10)

    comments = submission.comments.list()
    commentCounter = 0
    timeCounter = 0.0

    avatar = submission.author.icon_img
    response = requests.get(avatar)
    file = open(pathlib.Path(RESOURCES + "/images/avatar.png"), "wb")
    file.write(response.content)
    file.close()
    avatar = pathlib.Path(RESOURCES + "/images/avatar.png")
    
    for comment in comments:
        bod = comment.body
        author = comment.author
        
        if len(post_title) > 100:
            try:
                sendMail("skipped video due to long name", "skipped video: '{}' due to long name".format(post_title))
            except:
              print("skipped video due to long name", "skipped video: '{}' due to long name".format(post_title))
            exists = True
            break

        exists = False
        vidList = os.listdir(VIDEOS_DIR)
        vidnameMP4 = vidname + ".mp4"
        for vid in vidList:
            if vid == vidnameMP4:
                print("this video already exists, video from directory: {}, this video {}".format(
                    vid, vidnameMP4))
                exists = True
        if exists == True:
            break

        if timeCounter >= def_time:
            break
        if commentCounter >= commentLimit:
            break
        timeCounter = 0
        submissionList.append(bod)  # .replace("\n", "")
        print(submissionList[commentCounter])
        try:
            text_to_wav("en-US-Wavenet-B", submissionList[commentCounter], "comment{}".format(commentCounter))
        except:
            print("Resource Exhausted, skipping")
            commentCounter += 1
            continue
        screenshotter.reddit_ss = ("comment{}".format(commentCounter))
        imgdir = pathlib.Path(SAMPLE_INPUTS + '/imgs/' +
                              screenshotter.reddit_ss)
        screenshotter.createSS(submissionList[commentCounter], upImage, downImage, author)
        print(" - created comment ss -")
        path = os.path.join(SAMPLE_INPUTS, "audio")
        file = os.path.join(path, "comment{}".format(commentCounter) + ".wav")
        aud = WAVE(file)
        audio_info = aud.info
        duration = int(audio_info.length)
        output_video = os.path.join(
            SAMPLE_OUTPUTS, "output{}.mp4".format(commentCounter))
        try:
            video_creator.makeVideo(imgdir, file, output_video, duration)
            video_creator.flash(output_video, output_video)
        except Exception as e:
            print("video_creator.makeVideo: {}".format(e))
            try:
                sendMail("ERROR: video_creator.makeVideo or flash",
                        "video_creator.makeVideo: {}".format(e))
            except:
                print("ERROR: video_creator.makeVideo or flash",
                        "video_creator.makeVideo: {}".format(e))
        sorted_list = sorted(os.listdir(SAMPLE_OUTPUTS))
        for filename in sorted_list:
            file = os.path.join(SAMPLE_OUTPUTS, filename)
            out = VideoFileClip(file)
            timeCounter = timeCounter + out.duration
            print(timeCounter)
        commentCounter += 1
    try:
        if exists == True:
            try:
                sendMail("Skipped", "Skipped {}, it already exists".format(
                    vidname))
            except:
                print("Skipped", "Skipped {}, it already exists".format(
                    vidname))
        else:
            videoUp = VIDEOS_DIR + "/" + vidname + ".mp4"

            try:
                createThumb(post_title, vidname, avatar)
            except Exception as e:
                sendMail("HATA THUMBNAILDA", e)
                print("HATA THUMBNAILDA", e)
            
            thumbnailDir = SAMPLE_INPUTS + "/thumbnail/" + vidname + '.png'
            thumbdir = SAMPLE_INPUTS + "/thumbnail/" + vidname + ".png"

            try:
                SendMailAttached("Thumbnail created", "Thumbnail created for id: {}".format(vidname), thumbdir )
            except:
                print("Thumbnail created", "Thumbnail created for id: {}".format(vidname), thumbdir )
            video_creator.videomixer(vidname)
            try:
                sendMail("-Successfully finished creating video-",
                        "Video: {}.mp4 {} seconds, created with {} comments".format(vidname, timeCounter, commentCounter))
            except:
                print("-Successfully finished creating video-",
                        "Video: {}.mp4 {} seconds, created with {} comments".format(vidname, timeCounter, commentCounter))
            youtubeDataApiSample.main(post_title, "{} Enjoy...".format(post_title), videoUp, thumbnailDir)
            try:
                sendMail("Sent to Youtube", "Proccessing video upload. Your video will be uploaded to youtube in a few minutes.")
            except:
                print("Sent to Youtube", "Proccessing video upload. Your video will be uploaded to youtube in a few minutes.")
    except Exception as e:
        try:
            sendMail("Error occured", e)
        except:
            print("Error occured", e)



try:
    sendMail("DONE", "Latest Video Set Is Done, You Can Now Backup or Upload New Vids")
except:
    print("DONE", "Latest Video Set Is Done, You Can Now Backup or Upload New Vids")
sys.exit(0)

