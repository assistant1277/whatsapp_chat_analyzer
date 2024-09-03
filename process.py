from tkinter.font import names
from unicodedata import name
import pandas as pd
import re
import datetime as dt

import re 
# f=open("rajom.txt",'r',encoding="utf-8")
# data=f.read()

# print(data)
#writing this 
def process(data):

    #pat="\d{1,2}\/\d{1,2}\/\d{2,4}\,\s\d{1,2}\:\d{1,2}\s[am-pm]+"
    pat="\d{1,2}\/\d{1,2}\/\d{2,4}\,\s\d{1,2}\:\d{1,2}\s[am-pm]+"
    msg=re.split(pat,data)[1:]
    print(type(msg))
    print(msg)
    
    dates=re.findall(pat,data)
    #print(dates)
    
    ''''''
    df={"user-msg":msg, 'date':dates}
    df1=pd.DataFrame(df,columns=["user-msg","date"])
    #print(df1)
    
    
    #preprocessor
    user=[]
    msg1=[]
    for msg in df["user-msg"]:
        ent=re.split("(\-\s\w{0,10}\s\w{0,10}\:\s)",msg)
        if ent[1:]:
            user.append(ent[1])
            msg1.append(ent[2])
        else:
            user.append("group_notification")
            msg1.append(ent[0])    
    
    df1["user"]=user
    df1["message"]=msg1
    df1.drop(columns=["user-msg"],inplace=True)
    
    #print(df1)
    
    
    df1["date"]=pd.to_datetime(df['date'])
    df1["month_num"]=df1['date'].dt.month
    df1["only_date"]=df1['date'].dt.date
    df1["month"]=df1["date"].dt.month_name()
    df1["year"]=df1['date'].dt.year
    df1["hour"]=df1['date'].dt.hour
    df1["minute"]=df1['date'].dt.minute
    df1["day"]=df1['date'].dt.day
    df1["day_nam"]=df1['date'].dt.day_name()

    period=[]
    for hour in df1[["day_nam","hour"]]["hour"]:
        if hour==23:
            period.append(str(hour)+"-"+str("00"))
        elif(hour ==0):
            period.append(str("00")+"-"+str(hour+1))

        else:
            period.append(str(hour)+"-"+str(hour+1))        
    
    df1["period"]=period

    #print(df1)
    
    #df1["year"]=df1["date"].str.extract("") # extra
    
    return df1
