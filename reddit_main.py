import praw
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()


reddit = praw.Reddit(client_id='M8UOB3CGRiUmww',
                     client_secret='mCp7pbzuUelnB_zGdKztbTcvarA',
                     password='158303aTm',
                     user_agent='PyEng Boto 0.1',
                     username='coddins')

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

    msg = MIMEText(mail_gun())
    msg['From'] = 'kelechicollins93@yahoo.com'
    msg['To'] = 'kelechicollins93@gmail.com'
    msg['Subject'] = 'Subject: Reddit Top 10 daily.'

    try:
        smtpObj = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('kelechicollins93@yahoo.com', 'cmpztawzbohdqnpx')
        text = msg.as_string()
        smtpObj.sendmail('kelechicollins93@yahoo.com',
                         'kelechicollins93@gmail.com', text)
        print('successfully sent you the mail')
    except Exception as e:
        print('error', e)
    finally:
        print('disconnecting from SMTP SERVER')
        smtpObj.quit()


if __name__ == '__main__':
    sched.start()
