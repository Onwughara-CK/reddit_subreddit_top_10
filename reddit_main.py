import praw
#import yagmail
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()


reddit = praw.Reddit(client_id='x',
                     client_secret='x',
                     password='x',
                     user_agent='x',
                     username='x')

subs = [
    'learnpython', 'beermoney', 'slavelabour',
    'startups', 'iama', 'datascience', 'datasciencejobs', 'machinelearning',
    'workonline', 'mturk', 'SwagBucks'
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


@sched.scheduled_job('interval', minutes=1)
def send_mail():

    try:
        smtpObj = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('x', 'x')
        smtpObj.sendmail('x',
                         'x', 'Subject: Reddit Top 10 daily.\n\n' + mail_gun())
        print('successfully sent you the mail')
    except Exception as e:
        print('error', e)
    finally:
        print('disconnecting from SMTP SERVER')
        smtpObj.quit()


if __name__ == '__main__':
    sched.start()
