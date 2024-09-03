
from email import message
from operator import index
from optparse import Values
from os import renames, sep
#from turtle import pd
import urlextract as url
import wordcloud as wc
import collections as collect
import pandas as pd
import emoji as ei

extract=url.URLExtract()

def fetch(listv1,tf):

    '''
    if listv1=="overall":

         
        #1 no of msg
        # return tf.shape[0]
        #or
        #nomsg=len(tf)
        #or
        nomsg=tf.shape[0]

        word=[]
        for mess in tf['message']:
            word.extend(mess.split())

        return nomsg,len(word)
    
    else:

        newmsg=tf[tf["user"]==listv1]
        new1=newmsg.shape[0]

        word=[]
        for mess in new1['message']:
            word.extend(mess.split())

        return new1,len(word)

       #return tf[tf["user"]==listv1].shape[0]
       '''
#or

    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]   

    msg1=tf.shape[0] #1
    #or
    #msg1=tf["user"].count() #1

    words=[] #2
    for mess in tf["message"]:
        words.extend(mess.split(" "))

    nomedia1=tf[tf["message"]=="<Media omitted>"].shape[0]   # error 

    links=[]
    for mess in tf["message"]:
        links.extend(extract.find_urls(mess))
   
    return msg1,len(words),nomedia1,len(links)   


    
def most_busy(tf):
    x=tf.user.value_counts().head(6)

    dt2=round((tf.user.value_counts()/tf.shape[0])*100,2).reset_index().rename(columns={"index":"name","user":"percentage"})
    return x,dt2


def word_cloud(listv1,tf):
    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]  

    cloud=wc.WordCloud(width=400,height=400,min_font_size=9,background_color="white",max_words=15)
    tf_cloud=cloud.generate(tf["message"].str.cat(sep=" ")) # for breaking words
    return tf_cloud


def repeated_mess(listv1,tf):
    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]  

    words=[]
    for mess in tf["message"]:
        words.extend(mess.split(" "))
    
    col=pd.DataFrame(collect.Counter(words).most_common(20))

    return col   


def emoji_help(listv1,tf):
    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]  

    emoji=[]
    for mess in tf["message"]:
        for c in mess:
            if c in ei.EMOJI_DATA:
              emoji.extend(c) 
        

    et=pd.DataFrame(collect.Counter(emoji).most_common(40))
    # return pd.DataFrame(emoji)
    return et


def month(listv1,tf):
    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]  

    timeline=tf.groupby(["year","month_num","month"]).count()["message"].reset_index()
    
    ty=[]
    for i in range(timeline.shape[0]): #row
        ty.append(timeline["month"][i]+"-"+str(timeline["year"][i]))

    timeline["time"]=ty
    return timeline


def daily_time(list1v,tf):
        if list1v != "overall":
           tf=tf[tf["user"]==list1v]  
        
        timeline1=tf.groupby("only_date").count()["message"].head(10).reset_index()
        return timeline1


def week(list1v,tf):
       if list1v != "overall":
           tf=tf[tf["user"]==list1v]  

       timeline2=tf['day_nam'].value_counts()
       return timeline2
                 

def bmonth(list1v,tf):
       if list1v != "overall":
           tf=tf[tf["user"]==list1v]  

       timeline3=tf['month'].value_counts()
       return timeline3                 


def repeated_char(listv1,tf):
    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]  

    words=[]
    for mess in tf["message"]:
        for sts in mess:

           words.extend(sts.split(" "))
    
    cas=pd.DataFrame(collect.Counter(words).most_common(20))
    return cas 


def working_hour(listv1,tf):
    #Let’s check the most suitable hour of the day whenever there will be more chances of getting a response from group members 
    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]  

    hr_te = tf['hour'].value_counts().head(5)
    return hr_te 


def year_st(listv1,tf):
    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]  

    active_yr = tf['year'].value_counts().head(6)
    return active_yr     


def activity_map(listv1,tf):
    if listv1 != "overall":
        tf=tf[tf["user"]==listv1]  

    heat_map=tf.pivot_table(index='day_nam',columns='period', values="message",aggfunc="count").fillna(0)        

    return heat_map


