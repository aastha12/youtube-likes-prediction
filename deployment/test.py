import requests

video = {
        'index':12,
        'channelId':"UCeXY-D7RTVIIOuKP9HB35Ig",
        'videoCategoryId':10,
        'channelViewCount':25000,
        'videoCount':20, 
        'subscriberCount':200,
        'videoId':"--NZRkXBV7k",
        'channelelapsedtime':80000,
        'channelCommentCount':8,
        'videoViewCount':10000,
        'elapsedtime':22000, 
        'videoDislikeCount':1,
        'videoPublished':"2015-03-30T04:04:40.000Z", 
        'VideoCommentCount':2
        }

url = 'http://localhost:9696/predict'
response = requests.post(url, json=video)
print(response.json())
