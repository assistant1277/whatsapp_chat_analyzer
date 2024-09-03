from cProfile import label
from matplotlib.lines import lineStyles
import streamlit as st
import process
import help
#from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import requests
#from streamlit_lottie import st_lottie
import streamlit_lottie as slot

st.set_page_config(
    page_title="Whatsapp Group chat analyzer",
    page_icon="🏠",
    layout="wide"
)

page='''

<style>
.main{
    background-color:#111720
}

[data-testid="stSidebar"]{
    background-color:#10133d
}

.css-wq85zr{
    border:2px solid #0af10a
}

.css-1yjuwjr.effi0qh3{
    position:relative;
    left:60px
}


</style>

'''
st.markdown(page,unsafe_allow_html=True)


def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lot=load_lottie("https://assets9.lottiefiles.com/packages/lf20_6yIUKcHwko.json")
slot.st_lottie(lot,height=150,width=150,key="codu")


st.sidebar.title("whatsapp chat analyzer")
st.markdown("<h1 style='text-align:center; color:#47B5FF;'>Whatsapp Group Chat Analysis</h1>",unsafe_allow_html=True)
st.write("##")

upfile=st.sidebar.file_uploader("upload a file")
st.write("##")
if upfile is not None:
    data=upfile.getvalue()
    d1=data.decode("utf-8")
    # data=st.text(d1)
    tf=process.process(d1)
    st.dataframe(tf)

    list1=tf["user"].unique().tolist()
    #list1.remove("group_notification")
    list1.sort()
    list1.insert(0,"overall")
    
    list1v=st.sidebar.selectbox("show features: ",list1)

    if st.sidebar.button("show Analysis"):
        st.write("##")
        st.title("Total Statistics")
        number1,words1,nomedia,link1=help.fetch(list1v,tf)

        c1,c2,c4=st.columns(3)

        with c1:
            st.header("Total message: ")
            st.title(number1)

        with c2:
            st.header("Total words: ")
            st.title(words1)

        # with c3:
        #     st.header("Total medias: ")
        #     st.title(nomedia)    

        with c4:
            st.header("Total links: ")
            st.title(link1)    

        if list1v=="overall":
            st.write("---")
            #st.title("most busy user")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Most Busy User</h1>",unsafe_allow_html=True)
            x,dt1=help.most_busy(tf)
            fig,ax=plt.subplots()

            g1,g2=st.columns(2)
            with g1:
                ax.bar(x.index,x.values,linestyle=":",linewidth=3,color=['#FF731D', 'red', 'green', 'blue', 'cyan',"#FCE700","purple"])
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with g2:
                st.dataframe(dt1)


        with st.container():

            st.write("##")
            st.write("---")
            #st.title("Word Cloud")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Word Cloud</h1>",unsafe_allow_html=True)

            tf_cloud=help.word_cloud(list1v,tf)
            fig,bx=plt.subplots()
            bx.imshow(tf_cloud)
            st.pyplot(fig)


        with st.container():

            st.write("##")
            st.write("---")
            #st.title("Most repeated messages")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Most repeated messages</h1>",unsafe_allow_html=True)

            colo=help.repeated_mess(list1v,tf)
            fig,ax=plt.subplots()
            p1,p2=st.columns(2)

            with p1:
              st.write("##")
              st.dataframe(colo)
                                                                                          
            with p2:
                ax.barh(colo[0],colo[1])
                st.pyplot(fig)
        

        with st.container():
            st.write("##")
            st.write("##")
            st.write("---")
            #st.title("Most used Emojis")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Most used Emojis</h1>",unsafe_allow_html=True)

            pet=help.emoji_help(list1v,tf)
            e1,e2=st.columns(2)

            with e1:            
               st.dataframe(pet)

            with e2:
                fig,ax=plt.subplots()
                ax.pie(pet[1],labels=pet[0],autopct="%.2f",shadow = True) # passes only paarmeter
                plt.xticks(rotation="horizontal")
                plt.legend()
                st.pyplot(fig)  

        with st.container():

            st.write("##")
            st.write("##")
            st.write("---")
            #st.title("Monthly daily messages")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Monthly daily messages</h1>",unsafe_allow_html=True)

            ty=help.month(list1v,tf)
            fig,ax=plt.subplots()
            ax.plot(ty['time'],ty['message'],color="red",linestyle="dashed")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)                      

        with st.container():
            st.write("##")
            st.write("##")
            st.write("---")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Daily Timeline</h1>",unsafe_allow_html=True)

            ty=help.daily_time(list1v,tf)
            fig,ax=plt.subplots()
            ax.plot(ty['only_date'],ty['message'],color="black")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)         
        
        with st.container():
            st.write("##")
            st.write("##")
            st.write("---")
            #st.title("most busy day")
            #st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Most Busy day</h1>",unsafe_allow_html=True)
            w1,w2=st.columns(2)

            with w1:
                st.write("##")
                #st.subheader("Most busy month")
                st.markdown("<h3 style='text-align:center; color:#EEE3CB;'>Most Busy day</h3>",unsafe_allow_html=True)
                wek=help.week(list1v,tf)
                fig,ax=plt.subplots()
                ax.bar(wek.index,wek.values,color="orange")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)                             

            with w2:
                st.write("##")
                st.markdown("<h3 style='text-align:center; color:#EEE3CB;'>Most Busy Month</h3>",unsafe_allow_html=True)
                #st.subheader("Most busy month")
                busy_month=help.bmonth(list1v,tf)
                fig,ax=plt.subplots()
                ax.bar(busy_month.index,busy_month.values,color="violet")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)        

        with st.container():
            st.write("##")
            st.write("---")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Most repeated characters</h1>",unsafe_allow_html=True)

            colo=help.repeated_char(list1v,tf)
            fig,ax=plt.subplots()
            p1,p2=st.columns(2)

            with p1:
              st.write("##")
              st.dataframe(colo)
                                                                                          
            with p2:
                ax.barh(colo[0],colo[1])
                st.pyplot(fig) 


        with st.container():
            st.write("##")
            st.write("---")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Most working hour</h1>",unsafe_allow_html=True)

            olo=help.working_hour(list1v,tf)
            fig,ax=plt.subplots()
            o1,o2=st.columns(2)
            plt.xlabel('hours(24-hour)',fontdict={'fontsize': 12,'fontweight': 10})
            plt.ylabel('no of messages',fontdict={'fontsize': 12,'fontweight': 10})

            with o1:
              st.write("##")
              st.dataframe(olo)
                                                                                          
            with o2:
                ax.scatter(olo.index,olo.values)
                st.pyplot(fig) 
        

        with st.container():
            st.write("##")
            st.write("---")
            #st.title("Most repeated messages")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Most working year</h1>",unsafe_allow_html=True)

            olo=help.year_st(list1v,tf)
            fig,ax=plt.subplots()
            k1,k2=st.columns(2)
            plt.xlabel('year',fontdict={'fontsize': 12,'fontweight': 10})
            plt.ylabel('no of messages',fontdict={'fontsize': 12,'fontweight': 10})

            with k1:
              st.write("##")
              st.dataframe(olo)
                                                                                          
            with k2:
                #ax.scatter(olo.index,olo.values,color="red")
                ax = olo
                ax.plot.bar(color="#4C6793")
                st.pyplot(fig)                       


        with st.container():
            st.write("##")
            st.write("---")
            st.markdown("<h1 style='text-align:center; color:#EEE3CB;'>Weekly Activity Map</h1>",unsafe_allow_html=True)

            user_heat=help.activity_map(list1v,tf)
            fig,ax=plt.subplots()
            ax=sns.heatmap(user_heat)
            st.pyplot(fig)
        
