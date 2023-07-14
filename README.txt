This is a sample project Ecomm-Evadella-Dashboard.

Create Virtual Environment for the project by using "python -m venv venv".
Then clone the project from git clone "https://vamshi_bhairoju@bitbucket.org/dmantz/ecomdashboard.git."

Before run the project we have to import libraries.

 *import pickle
 *from pathlib import Path
 *import pandas as pd
 *import numpy as np
 *import streamlit as st
 *import mysql.connector
 *from streamlit_option_menu import option_menu
 *import streamlit_authenticator as stauth
 *from streamlit import session_state as state

After clone the project we have to install the above libraries.
For that have to install just requeriments.txt file which the libraries all mentioned, by using command "pip install -r requirements.txt".

There is a file generatekeys.py first run that file to create and secure the credentials like username and password.

Run the main file to run the project by using "streamlit evadellaapp.py". Then it will run in the port localhost:8501.
