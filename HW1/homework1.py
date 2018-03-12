#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import json
import wget
import sys
import io
import subprocess
import glob
import google.cloud.vision
import os

# Twitter API credentials
# Input your own credentials
consumer_key = 
consumer_secret = 
access_key = 
access_secret = 

#
twitter_account = "@ESPNNBA"

def get_all_tweets(screen_name):
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            break
        print("...%s tweets downloaded so far" % (len(alltweets)))
       
    '''#write tweet objects to JSON
    file = open('tweet.json', 'w') 
    print ("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)
    #close the file
    print ("Done")
    file.close()'''
    # get the image urls
    media_files = set()
    for status in alltweets:
        media = status.entities.get('media', [])
        if(len(media) > 0):
            media_files.add(media[0]['media_url'])
    
    # download the images
    i = 1
    for media_file in media_files:
        wget.download(media_file,'image'+str(i)+'.jpg')
        i += 1
    print("Images downloading done.")
    
    #os.system('ffmpeg -y -framerate 20 -i d:/graduate/ec500c1/image%d.JPG -pix_fmt yuv420p -filter:v "setpts=5.0*PTS" a.mp4')
    #os.system('PAUSE)

def ffmpeg():
    try: 
        subprocess.call('ffmpeg -y -framerate 20 -i image%d.JPG -pix_fmt yuv420p -filter:v "setpts=5.0*PTS" output.mp4', shell=True)
        print('Transforamtion from images to video done.')
    except (RuntimeError, TypeError,NameError):
        print("Can not create valid video.")
        pass


def googlelabels(description_count = 2):
	client = google.cloud.vision.ImageAnnotatorClient()

	outputdesc = {}

	for filename in glob.glob('*.jpg'):
		image_file_name = filename
		with io.open(image_file_name, 'rb') as image_file:
			content = image_file.read()

		# Use Vision to label the image based on content.
		image = google.cloud.vision.types.Image(content=content)
		response = client.label_detection(image=image)

		image_desc = []
		for label in response.label_annotations:
			if len(image_desc) < description_count:
				features = {}
				features['mid'] = label.mid
				features['description'] = label.description 
				features['score'] = str(label.score)
				features['topicality'] = str(label.topicality)
				image_desc.append(features)
			else:
				break
		if len(image_desc) == None:
			print ("There are no labels.")
		else:
			outputdesc[filename] = image_desc
	with open('labels.json','w') as outfile:
		json.dump(outputdesc, outfile, indent = 4, sort_keys = True)

	return outfile

def a():
    import io
    import os
    
    # Imports the Google Cloud client library
    from google.cloud import vision
    from google.cloud.vision import types
    
    # Instantiates a client
    GOOGLE_APPLICATION_CREDENTIALS = 'service-account-file.json'
    client = vision.ImageAnnotatorClient()
    
    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        './image*.jpg')
    
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    print('Labels:')
    for label in labels:
        print(label.description)

if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets(twitter_account)
    ffmpeg()
    googlelabels()
    #a()
    
