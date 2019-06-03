import feedparser, urllib, sys, json
import pprint

def log(input):
    with open("test.txt", "a") as myfile:
        myfile.write(input+"\n")

# pp = pprint.PrettyPrinter(indent=4)


# # d = feedparser.parse("http://feeds.feedburner.com/HemmerTime")
# # d = feedparser.parse("http://feeds.feedburner.com/foxnews/podcasts/FoxNewsSundayAudio/")
# d = feedparser.parse("https://www.the-american-interest.com/feed/podcast")
# # pp.pprint(len(d.entries))
# pp.pprint(d.entries[0])
# # print type(d.entries[0]


def trial():
    return "bob"

def retrieve():
    pp = pprint.PrettyPrinter(indent=4)
    # d = feedparser.parse("http://feeds.feedburner.com/HemmerTime")
    # # d = feedparser.parse("http://feeds.feedburner.com/foxnews/podcasts/FoxNewsSundayAudio/")
    d = feedparser.parse("https://www.the-american-interest.com/feed/podcast")
    # pp.pprint(len(d.entries))
    pp.pprint(d.entries[0])
    # print type(d.entries[0]


def getlists(input):
    # log("podcather:" + input)
    url = "https://itunes.apple.com/search?term={0}&entity=podcast&limit=100".format(input)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    # print data
    # for val in data['results']: 
    #     print val['artistName']
    #     print "{0} ({1})".format(val['artistName'].encode('utf8'), val['collectionName'].encode('utf8'))
    #     print "{0} ({1})".format(val['artistName'].encode('utf8'), val['collectionName'].encode('utf8'))
    return data
    # print "results", data['resultCount']
    # for idx, val in enumerate(data['results']):
    #     print "{0}. {1} ({2})".format(idx+1, val['artistName'].encode('utf8'), val['collectionName'].encode('utf8'))

# data = getlists("tim")
# print data['resultCount']
# print data['results'][0]
# for val in data['results']:
#     print val['artistName'].encode('ascii','ignore')
    # print "{0} ({1})".format(val['artistName'].encode('utf8'), val['collectionName'].encode('utf8'))



def addold():
    # return "added"
    with open("test.txt", "a") as myfile:
        myfile.write("appended text\n")

def add(input):
    with open("test.txt","a") as myfile:
        myfile.write(input)

