from django.shortcuts import render
from django.http import HttpResponse
from instagram.client import InstagramAPI
import datetime
import facebook
import requests
import sys
import operator
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import dateutil.parser as dateparser
from json import dumps, loads
from sorl.thumbnail import get_thumbnail
import random
import urllib

CONST_USER_FACEBOOK = "mexicogp"
EXTENDED_TOKEN_FACEBOOK = 'CAAZAHDZBd0zOkBAHrvHbRMi3zXiqKewGo8t7IasunEfHVWvWwzaTcG3quttqwExyZBjc645Mc6onEqb8BlLeeY6QBZAayXpVUUyXhJkkVvWQ2JNGmaF7bZCuaQAwdcL3HwYyBXTbVIx8GIU90vST6OZCOTPUCXArpi3NOKXyqAWWixy1QNd6BRJhgNiX2hW6UZD'

CONST_USER_TWITTER = "@mexicogp"
CONST_USER_LINK_TWITTER = "mexicogp"
CONSUMER_KEY_TWITTER = "MToutlg9vV08FKCQUoiwXFVmH"
CONSUMER_SECRET_TWITTER = "b9jhnaJuHdhoNBhEv8N7XHOWgiPvvpNDuBHlNjR7UEV4DFqxig"
ACCESS_TOKEN_TWITTER = "2167556856-RmZHrI1veXxozyuG07vNgm5V0q3pJHslTu7dCnI"
ACCESS_TOKEN_SECRET_TWITTER = "QhAkahpiUzNSB6A1rlPn2slqyjh9xkD11dinJoQXIqabg"

ACCESS_TOKEN_INSTAGRAM = "1296904443.e653774.41fb070a224e40fab914288678292b1d"
CLIENT_SECRET_INSTAGRAM = "1580722098914ae19056e65ddb69d846"
USER_ID_INSTAGRAM = '1681101575'
CONST_USER__INSTAGRAM = 'mexicogp'

COUNT_NUMBER_POST = 15
IMAGEN_FONDO_AZUL = "socialhub/fondo-azul.jpg"

BACKGROUND_COLOR_POST_IMAGE= "#e1e3e3"


def get_picture_facebook(request):
    data= 'fail'
    if request.is_ajax():
        post_id = request.POST.get('post_id', 0)
        print post_id
        #try:
        url = "https://graph.facebook.com/v2.6/" + post_id + "?fields=full_picture,link&access_token=" + EXTENDED_TOKEN_FACEBOOK
        r = requests.get(url)
        r_json = r.json()
        full_picture = ''
        link = ''
        if 'full_picture' in r_json:
            full_picture = r_json["full_picture"]
        if 'link' in r_json:
            link  = urllib.quote_plus(str(r_json["link"]))

        data = {"id":post_id,"picture":full_picture,"link":link}
        #except Exception, e:
            #data = 'fail'
    print "data"
    print data
    return HttpResponse(dumps(data), 'application/json')

def get_randon_image():
    image = ''.join(random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']))
    image = "socialhub/social-hub-gulf-mexico" + image + ".jpg"
    return image


def FeedFacebook(request):
    graph = facebook.GraphAPI(EXTENDED_TOKEN_FACEBOOK)
    profile = graph.get_object(CONST_USER_FACEBOOK)
    feed = graph.get_connections(profile['id'], 'posts')
    posts = []
    try:
        [posts.append({"id":p["id"],"created_time":datetime.datetime.strptime(p["created_time"], '%Y-%m-%dT%H:%M:%S+0000'),
                       "message":p["message"],"text_encoded":p["message"],"type":"facebook","image":IMAGEN_FONDO_AZUL,"link":"",
                       "link_encoded":""}) for p in feed['data']]
    except Exception, e:
        pass

    return posts


def FeedTwitter():
    auth = OAuthHandler(CONSUMER_KEY_TWITTER, CONSUMER_SECRET_TWITTER)
    auth.set_access_token(ACCESS_TOKEN_TWITTER, ACCESS_TOKEN_SECRET_TWITTER)
    api = API(auth)
    feed = api.user_timeline(screen_name=CONST_USER_TWITTER, count=COUNT_NUMBER_POST, page=1, include_rts=True)
    tweets = []
    for t in feed:
        if t.in_reply_to_status_id == None:
            try:
                tweet = {"text": t.text, "text_encoded": t.text, "type": "tweet", "created_time": t.created_at,
                         "link":"https://twitter.com/"+CONST_USER_LINK_TWITTER+"/status/" + str(t.id),
                         "link_encoded":urllib.quote_plus("https://twitter.com/"+CONST_USER_LINK_TWITTER+"/status/" + str(t.id)),
                         "user": {"name": t.user.name, "screen_name": "@" + t.user.screen_name,"profile_image":t.user.profile_image_url}}
                if "media" in t.entities:
                    if t.entities['media'][0]['type'] == 'photo':
                        tweet["image"] = t.entities['media'][0]['media_url']
                    else:
                        pass
                        #print t.entities['media'][0]['type']
                else:
                    pass
                    #tweet["image"] = get_randon_image()
                tweets.append(tweet)
            except Exception, e:
                #print(str(e))
                pass
    return tweets

def FeedInstragram():
    api = InstagramAPI(access_token=ACCESS_TOKEN_INSTAGRAM, client_secret=CLIENT_SECRET_INSTAGRAM)
    posts = []
    feed, next_ = api.user_recent_media(user_id=USER_ID_INSTAGRAM, count=COUNT_NUMBER_POST)
    try:
        [posts.append(
            {"created_time": p.created_time, "type": "instagram", "user": p.user,
             "text": str(p.caption).replace("Comment: "+ CONST_USER__INSTAGRAM +" said ", ""),
             "text_encoded": str(p.caption).replace("Comment: gulfmexico said ", ""),
             "media_type": p.type, "link": p.link, "link_encoded": urllib.quote_plus(str(p.link)),
             "image": p.get_standard_resolution_url}) for p in feed]
    except Exception, e:
        pass
    return posts


def getposts(request):
    lists = FeedFacebook(request) + FeedTwitter() + FeedInstragram()
    #lists = FeedFacebook(request) + FeedInstragram()
    feeds = sorted(lists, key=lambda k: k['created_time'], reverse=True)

    return render(request, 'socialhub.html', {"posts":feeds})


