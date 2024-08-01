import streamlit as st

st.set_page_config(layout="wide")

#######################
# Page Navigation Set Up
#######################
portfolio = st.Page(
    "pages/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "pages/mls.py",
    title="Data Scouting Tool",
    icon=":material/tactic:",
)

#######################
# Page Navigation Sections
#######################
page = st.navigation(
    {
        "About Me": [portfolio],
        "Project Examples": [project_1_page]
    }
)

#######################
# Assets
#######################
st.logo('assets/logo.png')
st.sidebar.markdown("Made by <a href='https://www.linkedin.com/in/matthewrichardsdata/' style='color:orange;'>Matthew</a>", unsafe_allow_html=True)

#######################
# Run Navigation
#######################
page.run()