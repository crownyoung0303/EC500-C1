import tweepy
import json
import wget
import requests
import io
import os
import glob
from os import listdir
from google.cloud import vision
from google.cloud.vision import types
import sys

# input your own credentials
consumer_key = 
consumer_secret = 
access_key = 
access_secret = 


def get_all_tweets(screen_name):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=10)
    if len(new_tweets) == 0:
        print('The user did not tweet anything.')
        txt = open('bad_result.txt', 'w')
        txt.write('The user did not tweet anything.')
        txt.close()
        sys.exit()

    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:

        new_tweets = api.user_timeline(
    screen_name=screen_name, count=10, max_id=oldest)

        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            print('more that 15 tweets downloaded.')
            break
        print("There are %s tweets downloaded so far" % (len(alltweets)))

    media_files = set()

    for status in alltweets:
        try:
            media = status.extended_entities.get('media', [])
        except:
            media = status.entities.get('media', [])
        if(len(media) > 0):
            for i in range(len(media)):
                media_files.add(media[i]['media_url'])
    if len(media_files) == 0:
        print('The user did not post any pictures.')
        txt = open('bad_result.txt', 'w')
        txt.write('The user did not post any pictures.')
        txt.close()
        sys.exit()
    for media_file in media_files:
        wget.download(media_file)


def writefile(name):
    GOOGLE_APPLICATION_CREDENTIALS = './service-account-file.json'
    client = vision.ImageAnnotatorClient()
    f_name = str(name) + '_result.txt'
    file = open(f_name, 'w')
    m = 1
    OBJ = []
    for pic in listdir("."):
        if pic.endswith('jpg') or pic.endswith('png'):
            OBJ.append(pic)
    print(str(len(OBJ)) + ' Pictures Found.' + '\n')
    file.write('Below is the pictures info detected of user: "@' +
    name +
    '"' +
     '\n')
    file.write(str(len(OBJ)) + ' Pictures Found.' + '\n')
    if len(glob.glob("*.png")) >= 1 and len(glob.glob("*.jpg")) >= 1:
        os.system('ffmpeg -framerate 1 -pattern_type glob -i "*.png"   -c:v libx264 -r 30 -pix_fmt yuv420p 2.mpg')
        os.system('ffmpeg -framerate 1 -pattern_type glob -i "*.jpg"   -c:v libx264 -r 30 -pix_fmt yuv420p 1.mpg')
        os.system('cat 1.mpg 2.mpg | ffmpeg -f mpeg -i - -qscale 0 -vcodec mpeg4 output.mp4')
        # os.system('cat 1.mpg 2.mpg | ffmpeg -f mpeg -i - -qscale 0 -vcodec mpeg4 output1.mp4')
        os.remove('1.mpg')
        os.remove('2.mpg')
    if len(glob.glob("*.jpg")) >= 1 and len(glob.glob("*.png")) == 0:
        os.system('ffmpeg -framerate 1 -pattern_type glob -i "*.jpg"   -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4')
    if len(glob.glob("*.jpg")) == 0 and len(glob.glob("*.png")) >= 1:
        os.system('ffmpeg -framerate 1 -pattern_type glob -i "*.png"   -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4')
    os.system("cp output.mp4 ./static")
    for i in OBJ:
        file_name = os.path.join(os.path.dirname(__file__), i)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        # writing Picutre names and  IDs to txt.file
        print('Picture Name: ' + i + ', ID: ' + str(m))
        print(str(len(labels)) + ' objects detected.')
        print('Labels:')
        file.write('Picture Name: ' + i + ', ID: ' + str(m) + '\n')
        file.write(str(len(labels)) + ' objects detected.' + '\n')
        file.write('Labels:' + '\n')
        m = m + 1
        for label in labels:
            file.write(label.description + '\n')
            print(label.description)
        print('')
        file.write('\n')
    file.close()

# get_all_tweets("@ESPNNBA")


def main():
    name = input('Please Enter Account:\n')
    names = '@' + str(name)
    if str(name) == 'quit':
    	print('The program ends')
    	sys.exit()
    try:
        get_all_tweets(name)
    except tweepy.error.TweepError:
        txt = open('error.txt', 'w')
        txt.write('The user does not exist.')
        txt.close()
        print('The user does not exist')
        
        sys.exit()

    writefile(name)
if __name__=='__main__':
    main()
