from twitter import Twitter
import time

#testing push ke heroku
#fsfnjinajia

tw = Twitter()

def start():
    print("Starting program...")
    dms = list()
    while True:
        if len(dms) != 0:
            for i in range(len(dms)):
                message = dms[i]['message']
                sender_id = dms[i]['sender_id']
                id = dms[i]['id']

                if len(message) != 0 and len(message) < 280:
                    if"[trigger]" in message:
                        #message = message.replace("[trigger]", "[rplcdtrigger]")
                        if len(message) != 0:
                            if dms[i]['media'] is None:
                                print("DM will be posted")
                                tw.post_tweet(message)
                                tw.delete_dm(id)
                            else:
                                print("DM will be posted with media")
                                tw.post_tweet_with_media(message, dms[i]['media'])
                                tw.delete_dm(id)
                        else:
                            print("DM deleted because its empty...")
                            tw.delete_dm(id)
                    else:
                        print("DM will be deleted because doesn't contains keyword...")
                        tw.delete_dm(id)
            dms=list()
        else:
            print("Direct message is empty...")
            dms = tw.read_dm()
            if len(dms) <= 0:
                time.sleep(60)

if __name__=="__main__":
    start()