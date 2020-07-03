#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
consumer_key = "kOd64GqfyxZ3cPkAcJ5pmzpue"
consumer_secret = "k2eslhHKFaI1OOY7v6GyOzRvvkZGyQeGZ6igIgjnIRZQlZjdNs"
access_token = "1172585074123923456-ICjJAILHR4aHQZAPp0dHE2f0G3Pvap"
access_token_secret = "YfukRoA7MFqqpehUJoJ2ghtn3INaSBOB7mDs3rU94Pqwg"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        file = open("twitter.txt","a",encoding="utf-8")
        file.write(data+"\n")
        self.counter += 1
        file.close()
        if self.counter < self.limit:
            return True
        else:
            stream.disconnect()
            return False

    def on_error(self, status):
        print (status)
    
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 5

#This handles Twitter authetification and the connection to Twitter Streaming API
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

def TwitterDataExtraction(additional_words):
    stoplists=[]
    stoplists += additional_words.split(" ")
    print(stoplists)
    #This line filter Twitter Streams to capture data by the keywords:
    stream.filter(track=stoplists)
    # spliting the string into words
    totalWordsMatch=0
    # create a dictionary for all search words, setting each count to 0
    count = dict.fromkeys(stoplists, 0)
    print("initial dictionary",count)
    # find the word in the text file and save that line in another file
    F1 = open('twitter.txt', 'r',encoding="utf-8")
    for line in F1:
        for word in stoplists:
            if word.lower() in line.lower():
                # found a word you wanted to count, so count it
                count[word] += 1
    F1.close()
    print("final dictionary",count)
    totalWordsToMatch = len(count)
    for i in count:
        if count[i]!=0:
            totalWordsMatch+=1
    percentageOfWordsMatch = totalWordsMatch/totalWordsToMatch
    return percentageOfWordsMatch