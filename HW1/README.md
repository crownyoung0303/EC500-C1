# EC500-C1 Homework 1

## Project Goals
- Twitter API to access the twitter content</br  >
- FFMPEG to convert images to videos</br  >
- Google Vision analysis to describe the content</br  >

## How to run the program:
1. Download homework1.py
2. Install [Tweepy](https://github.com/tweepy/tweepy)
```
pip install tweepy
```
3. Install [FFMpeg](https://www.ffmpeg.org/)<br />
Because my program is ran on windows, we should also change the environment variables.
4. Install Wget
```
pip install wget
```
5. Get your credentials and access token from your twitter account [here](https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/)
6. Put your token information into homework1.py
7. Change the twitter account from which you want to get images<br />
8. Install google cloud for python
```
pip install google-cloud-python
```
9. Get your Google Vision API Credentials [here](https://cloud.google.com/vision/docs/auth)
```
First, open a gcp project in the console.
Second, create credentials in the APIs & Services and download it.
Last, change the json file name to 'service-account-file.json' that are corresponding to the homework1.py.
```
10. Run the homework1.py <br />
We will get an output.mp4 which consists of the images downloaded using tweepy.
Additionally, we can get the labels of the images using the google cloud vision api.

### Feel free to ask me any questions: yls@bu.edu

