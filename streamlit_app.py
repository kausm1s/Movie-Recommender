import streamlit as st
import streamlit_lottie
import requests
from streamlit_lottie import st_lottie
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import time

global_final_movie_list = []

st.set_page_config(page_title="Movie Reccomendation system", page_icon="movie_camera",layout="centered")


with open('saved_model.pkl', 'rb') as file:
    data=pickle.load(file)


knn_model=data['model']
movie_list=data['movie_list']
weightage_list=data['weightage_list']
mean_rating=data['mean_rating']
df_movie=data['df_movie']
movie_ids=data['movie_ids']
mov_t=data['mov_t']
rf_dataset=data['rf_dataset']



def load_animation(url):
    r=requests.get(url)
    return r.json()



lottie_code= load_animation("https://assets3.lottiefiles.com/private_files/lf30_bb9bkg1h.json")

# HEADER
st.subheader("This is our Pattern Recognition & Machine Learning Course Project")
st.title("Movie Recommendation System")


with st.container():
    st.write("---")
    left_column,right_column = st.columns(2)
    with left_column:
        st.header("How it Works")
        st.write('''Behind the web application, a machine learning model (KNN) that 
                    has been trained on IMDb's dataset, tries to predict which users
                    are the most similiar to the given user and then recommends movies
                    based on the top rated movies of those similiar users.''')

    with right_column:
        st.write('##')
        st_lottie(lottie_code,height=200,width=400,quality='high',key="watch_movie")


st.write("---")

user_id=int(st.number_input("Enter UserID",key="user_id",min_value=0,max_value=609))
st.write("##")
n_movies=int(st.slider("How many movies do you want to see?", min_value=1, max_value=10, value=2,key="n_movies"))

from pprint import pprint


def recommender_system(user_id, n_similar_users, n_movies): #, user_to_movie_df, knn_model):
  

  # def get_similar_users(user, user_to_movie_df, knn_model, n = 5):
  def similar_users(userId,n_users=10):
    knn_input=np.asarray([df_movie.values[userId-1]])
    dists,idxs=knn_model.kneighbors(knn_input,n_neighbors=n_users+1)
    
    print(f'Top {n_users} users who are the most similar to user {userId} are: ')
    for i in range(1,len(dists[0])):
      print(f'{i} User {idxs[0][i]+1} separated by distance of {dists[0][i]}')
    return idxs.flatten()[1:]+1,dists.flatten()[1:]


  def filtered_movie_recommendations(n):
  
    first_zero_index = np.where(mean_rating == 0)[0][-1]
    sortd_index = np.argsort(mean_rating)[::-1]
    sortd_index = sortd_index[:list(sortd_index).index(first_zero_index)]
    n = min(len(sortd_index),n)
    movies_watched = list(rf_dataset[rf_dataset['userId'] == user_id]['title'])
    filtered_movie_list = list(movie_list[sortd_index])
    count = 0
    final_movie_list = []
    for i in filtered_movie_list:
      if i not in movies_watched:
        count+=1
        final_movie_list.append(i)
      if count == n:
        break
    if count == 0:
      print("There are no movies left which are not seen by the input users and seen by similar users. May be increasing the number of similar users who are to be considered may give a chance of suggesting an unseen good movie.")
    else:
      for i in final_movie_list:
        print(i)
        global_final_movie_list.append(i)

  similar_user_list, distance_list = similar_users(user_id,n_similar_users)
  weightage_list = distance_list/np.sum(distance_list)
  sim_users_ratings = df_movie.values[similar_user_list]
  movies_list = df_movie.columns
  movie_list=[]
  for i in range(len(movie_ids)):
    movie_list.append(mov_t.loc[mov_t['movieId']==movie_ids[i]]['title'])
  movie_list=np.array(movie_list)
  movie_list=movie_list.flatten()
  weightage_list = weightage_list[:,np.newaxis] + np.zeros(len(movies_list))
  new_rating_matrix = weightage_list*sim_users_ratings
  mean_rating_list = new_rating_matrix.sum(axis =0)
  print("")
  print("Movies recommended based on similar users are: ")
  print("")
  filtered_movie_recommendations(n_movies)

with st.spinner('Syncing changes...'):
    recommender_system(user_id,10,n_movies)
st.success('Synced with server!')

ok1 = st.button("See top recommended movies")
if ok1:
    with st.container():
        st.write("---")
        left_column,right_column = st.columns(2)

        with right_column:
            lottie_code= load_animation("https://assets3.lottiefiles.com/packages/lf20_cbrbre30.json")
            st_lottie(lottie_code,height=200,width=375,quality='high',key="heart_load")

        with left_column:
            st.header("Calculating Recommendations...")
            time.sleep(1)
            st.write("Feeding Data to Model...")
            time.sleep(1)
            st.write("Making Predictions...")
            time.sleep(1)
            st.write("Retrieving Data...")
            time.sleep(1)
    

    with st.container():
        st.write("---")
        left_column,right_column = st.columns(2)

        with right_column:
            lottie_code= load_animation("https://assets3.lottiefiles.com/packages/lf20_khzniaya.json")
            st_lottie(lottie_code,height=200,width=375,quality='high',key='good')

        with left_column:
            st.subheader("Here are the top recommended movies for you:")
            for i in global_final_movie_list:
                st.write(i)

# with st.container():

#     left_column,right_column = st.columns(2)
#     with left_column:
#         st.header("Behavorial Survey")
#         st.write("Fill the Short Survey below to get a prediction of your heart disease risk. Your data is not collected or stored anywhere.")
#         st.write("---")


#     with right_column:
#         lottie_code= load_animation("https://assets4.lottiefiles.com/packages/lf20_tutvdkg0.json")
#         st_lottie(lottie_code,height=200,width=400,quality='high',key="survey")

# st.write("Are you Male or Female?")
# checkbox_9=st.checkbox("Male",key="male")
# checkbox_10=st.checkbox("Female",key="Female")
# if checkbox_9:
#     sex="Male"
# elif checkbox_10:
#     sex="Female"
# else:
#     sex="Female"

# st.write("##")
# age=st.select_slider("What is your Age Group?",options=["18-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59","60-64","65-69","70-74","75-79","80 or older"])
# height=st.slider("What is your Height in cm?",1,250,1)
# weight=st.slider("What is your Weight in Kg?",1,250,1)
# bmi=weight/((height/100)**2)

# ok1 = st.button("Check your BMI")
# if ok1:
#     bmi=weight/((height/100)**2)
#     st.write("Your BMI is:",bmi)


# st.write("##")
# st.write("Have you smoked over 100 cigarettes in your life?")
# checkbox_1 = st.checkbox("Yes",key="checkbox_1")
# checkbox_2 = st.checkbox("No",key="checkbox_2")
# if checkbox_1:
#     cig = "Yes"
# elif checkbox_2:
#     cig = "No"
# else:
#     cig = "No"



# st.write("##")
# st.write("Do you Consume Alcoholic Drinks Heavily? (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week")
# checkbox_3 = st.checkbox("Yes",key="checkbox_3")
# checkbox_4 = st.checkbox("No",key="checkbox_4")
# if checkbox_3:
#     alc="Yes"
# elif checkbox_4:
#     alc="No"
# else:
#     alc="No"


# st.write("##")
# st.write("Have you ever had a Stroke?")
# checkbox_5=st.checkbox("Yes",key="checkbox_5")
# checkbox_6=st.checkbox("No",key="checkbox_6")
# if checkbox_5:
#     stroke="Yes"
# elif checkbox_6:
#     stroke="No"
# else:
#     stroke="No"



# st.write("##")
# st.write("For how many days during the past 30 days was your physical health not good? (Injury/Illness)")
# phy_health=st.slider("Days",0,30,1,key="phy_health")



# st.write("##")
# st.write("For how many days during the past 30 days was your mental health not good?")
# mental_health=st.slider("Days",0,30,1,key="mental_health")



# st.write("##")
# st.write("Do you have difficulty walking or climbing stairs?")
# checkbox_7=st.checkbox("Yes",key="checkbox_7")
# checkbox_8=st.checkbox("No",key="checkbox_8")
# if checkbox_7:
#     walk="Yes"
# elif checkbox_8:
#     walk="No"
# else:
#     walk="No"


# st.write("##")
# st.write("Have you ever been diagnosed with any of the following?")
# checkbox_11=st.checkbox("Diabetes",key="diabetes")
# checkbox_18=st.checkbox("Yes (during pregnancy)",key="preg")
# checkbox_17=st.checkbox("No, borderline diabetes",key="bd")
# checkbox_12=st.checkbox("Asthma",key="asthma")
# checkbox_13=st.checkbox("Kidney Disease",key="kidney")
# checkbox_14=st.checkbox("Skin Cancer",key="cancer")

# if checkbox_17:
#     diabetes="No, borderline diabetes"


# if checkbox_18:
#     diabetes="Yes (during pregnancy)"


# if checkbox_11:
#     diabetes="Yes"
# else:
#     diabetes="No"


# if checkbox_12:
#     asthma="Yes"
# else:
#     asthma="No"


# if checkbox_13:
#     kidney="Yes"
# else:
#     kidney="No"


# if checkbox_14:
#     cancer="Yes"
# else:
#     cancer="No"


# st.write("##")
# st.write("Did you perform any sort of significant physical activity/exercise other than regular work in the past 30 days?")
# checkbox_15=st.checkbox("Yes",key="checkbox_30")
# checkbox_16=st.checkbox("No",key="checkbox_31")
# if checkbox_15:
#     excercise="Yes"
# elif checkbox_16:
#     excercise="No"
# else:
#     excercise="No"



# st.write("##")
# st.write("How many hours of sleep do you usually get in a 24hr time period?")
# sleep=st.slider("Hours",0,24,1,key="sleep")



# st.write("##")
# st.write("How would you rate your overall health?")
# health=st.select_slider("Choose an option",options=["Poor","Fair","Good","Very good","Excellent"],key="health")


# ok2 = st.button("Check Your Heart's Health")
# if ok2:
#     df=[bmi,cig,alc,stroke,phy_health,mental_health,walk,sex,age,diabetes,excercise,health,sleep,asthma,kidney,cancer]
#     columns=['BMI',	'Smoking','AlcoholDrinking','Stroke','PhysicalHealth','MentalHealth','DiffWalking','Sex','AgeCategory','Diabetic','PhysicalActivity','GenHealth','SleepTime','Asthma','KidneyDisease','SkinCancer']
#     df= pd.DataFrame([df],columns=columns)

#     df['Smoking']=le_smoking.transform(df['Smoking'])
#     df['AlcoholDrinking']=le_alcohol.transform(df['AlcoholDrinking'])
#     df['Stroke']=le_stroke.transform(df['Stroke'])
#     df['DiffWalking']=le_walk.transform(df['DiffWalking'])
#     df['Sex']=le_sex.transform(df['Sex'])
#     df['AgeCategory']=le_age.transform(df['AgeCategory'])
#     df['Diabetic']=le_diabetes.transform(df['Diabetic'])
#     df['PhysicalActivity']=le_exercise.transform(df['PhysicalActivity'])
#     df['GenHealth']=le_health.transform(df['GenHealth'])
#     df['Asthma']=le_asthma.transform(df['Asthma'])
#     df['KidneyDisease']=le_kidney.transform(df['KidneyDisease'])
#     df['SkinCancer']=le_cancer.transform(df['SkinCancer'])
  

#     normalisecolumns=['BMI','PhysicalHealth','MentalHealth','SleepTime']
#     df[normalisecolumns] = scaler.transform(df[normalisecolumns])

#     pred=model.predict(df)
#     percentpred=model.predict_proba(df)
#     with st.container():
#         st.write("---")
#         left_column,right_column = st.columns(2)

#         with right_column:
#             lottie_code= load_animation("https://assets5.lottiefiles.com/packages/lf20_GZVTNZ.json")
#             st_lottie(lottie_code,height=200,width=375,quality='high',key="heart_load")

#         with left_column:
#             st.header("Calculating...")
#             time.sleep(1)
#             st.write("Feeding Data to Model...")
#             time.sleep(1)
#             st.write("Making Predictions...")
#             time.sleep(1)
#             st.write("Retrieving Data...")
#             time.sleep(1)

    
#     if pred[0]==0:
#         with st.container():
#             st.write("---")
#             left_column,right_column = st.columns(2)

#             with right_column:
#                 lottie_code= load_animation("https://assets2.lottiefiles.com/packages/lf20_afs4kbqm.json")
#                 st_lottie(lottie_code,height=200,width=375,quality='high',key='good')

#             with left_column:
#                 st.subheader("Your Heart's Health is Good!")
#                 st.write("Good Job! The probability of you developing a heart disease is: ",percentpred[0][1]*100,"%")

                


            

        
#     else: 
#         with st.container():
#             st.write("---")
#             left_column,right_column = st.columns(2)

#             with right_column:
#                 lottie_code= load_animation("https://assets3.lottiefiles.com/private_files/lf30_yABbl9.json")
#                 st_lottie(lottie_code,height=200,width=375,quality='high',key="bad")

#             with left_column:
#                 st.subheader("Uh oh! Your Heart's Health is not Good!")
#                 st.write("Do not panic, Seek Medical Help. The probability of you developing a heart disease is: ",percentpred[0][1]*100,"%")

#     time.sleep(2)
#     st.write("---")
#     github_icon=("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png")
#     github_link=("https://github.com/amanthakur64/HeartDiseasePrediction")
#     st.markdown(f"""<a href={github_link}><img src={github_icon} alt="drawing" width="50"/></a>""",unsafe_allow_html=True,)





