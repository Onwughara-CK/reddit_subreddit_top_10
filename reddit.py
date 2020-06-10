import praw
import yagmail
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

# register an app on reddit to get the client id, client secret. user_agent is arbitrary
reddit = praw.Reddit(client_id='xxxxxxx',
                     client_secret='xxxxxxxxxxx',
                     user_agent='xxxxxxxxxx'
                     )

subs = [
    'learnpython',
    'startups', 'iama', 'datascience', 'datasciencejobs', 'machinelearning'
]


def mail_gun():
    mail = ''
    for sub in subs:
        mail += f'''
        \n\n
        ------------------------------------
        {sub}
        ------------------------------------
       
        '''
        top_10 = reddit.subreddit(sub).top('day', limit=10)
        for post in top_10:
            mail += f'''
        ----------------------------------------------
        TITLE: {post.title}  
        .......
        LINK: {post.url} 
        .......
        SUBREDDIT: {sub}           
                    '''
    return mail


@sched.scheduled_job('interval', hours=24)
def send_mail():
    try:
        # your gmail address and password. but you must set your gmail address to allow less secure apps.
        yag = yagmail.SMTP(user='xxxxxxx',
                           password='xxxxxxxxx')

        yag.send(to='xxxxxxxxxxxxx',
                 subject='Reddit Top 10 daily', contents=mail_gun())
    except:
        print("Error, email was not sent")


if __name__ == '__main__':
    sched.start()
