import datetime

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title = "Streamlit Design Page",
    layout = "wide"
)

st.title('Python Design Page')
df = pd.DataFrame({"SID" : [1,2,3,4,5], "Color" : ["Orange","blue","Green ","Pink","Red"] })
st.dataframe(df)

n = st.number_input("Enter the number of Entries: ",min_value=1,max_value = 10,step= 1)
st.markdown(n)
st.write(f'Number of Entries: {n}')
st.subheader(f'Header: {n}')
st.caption("This is the learning page")

level = st.text_input("Enter your level in Python(low, medium, high)")
st.write(level)

b_class = st.text_area("Enter your description")
st.write(b_class)

if st.button("Login"):
    st.success("You logged in")
role = st.selectbox("Enter your Interest",["backEnd","frontEnd","Android Developer","AWS Cloud Developer"])
st.subheader(role)

skills = st.multiselect("Enter your Skills",["c", "python", "java", "db", "javascript"])
st.subheader(skills)

goal = st.checkbox("Run 10km")
if goal:
    st.success("Congratulations!")

chai_base = st.radio("Enter your Chai Base",["Milk","Water","Sugar"])
st.markdown(chai_base)

coding_level = st.slider("Enter your Coding year of Experience",0,30,0)
if coding_level:
    st.success(f"Your Coding Year of Experience is {coding_level}")


dob = st.date_input("Enter your Date of Birth: ",datetime.date.today())
if dob:
    st.write(f"Your DOB is {dob}")
your_age = datetime.date.today() - dob
if your_age:
    st.success(f"Your {your_age} Years old!")


col1, col2 = st.columns(2)
with col1:
    st.header("C++")
    vote1 = st.button("Vote for C++")
    st.image("https://i.pinimg.com/1200x/82/86/3e/82863e5e6e9e315fc84b86bd220db5b5.jpg",width=250)

with col2:
    st.header("Python")
    vote2 = st.button("Vote for Python")
    st.image("https://i.pinimg.com/736x/42/e7/bf/42e7bfc9634d8daf3f184c8e67e737fd.jpg",width = 250)

if vote1:
    st.success("Thanks for choosing C++")
elif vote2:
    st.success("Thanks for choosing Python")

name = st.sidebar.text_input("Enter your name")
language = st.sidebar.selectbox("Enter your language",["C++", "Python","Java"])
st.sidebar.write(f"Hello {name}, thank's for choosing {language}")


