import streamlit_authenticator as stauth
from pathlib import Path
import pickle
import streamlit as st
# from evadellaapp import *
import pandas as pd
import hashlib
from streamlit import session_state as state

# user authentication
names = ["Giridhar", "Yerra"]
usernames = ["evadellagiri", "evadellayerra"]


file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
    
    credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":hashed_passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":hashed_passwords[1]
                }            
            }
        }

authenticator = stauth.Authenticate(credentials,
    "dashborad", "abcdefg", cookie_expiry_days = 30)

name, authentication_status, username = authenticator.login("login", "main")

# if state.authentication_status:
#     return

if authentication_status == False:
    st.error("Username/Password is incorrect")


if authentication_status:
    state.authentication_status = True
    st.success("You have successfully logged in.")
    authenticator.logout("logout")

    
    