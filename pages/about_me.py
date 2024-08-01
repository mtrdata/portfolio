import streamlit as st
from streamlit_extras.colored_header import colored_header

#######################
# Heading Columns
#######################
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile_image.png", width=230)

with col2:
    colored_header(
        label="Matthew Richards",
        description="Data Analyst with a passion for sport ⚽",
        color_name="orange-70",
    )
    st.markdown("<a href='https://github.com/mtrdata555' style='color:orange;'>GitHub</a> 💾", unsafe_allow_html=True)
    st.markdown("<a href='https://www.linkedin.com/in/matthewrichardsdata/' style='color:orange;'>LinkedIn</a> 🔗", unsafe_allow_html=True)
    
#######################
# Experience & Qualifications
#######################
st.write("\n")
colored_header(
    label="Experience & Qualifications",
    description="",
    color_name="orange-70",
    )
st.write(
    """
    - **Computer Science (BSc)** from Lancaster University
    - Scouting certifications from the **Professional Football Scouts Association** & the **Football Association**
    - **13 years** experience as a live events presenter
    - Experience working with high profile clients such as **Nintendo**, **Red Bull** & **Microsoft**
    - Excellent **problem-solving skills** & Strong **analytical skills**
    """
)

#######################
# Technical Skills
#######################
st.write("\n")
colored_header(
    label="Technical Skills",
    description="",
    color_name="orange-70",
    )
st.write(
    """
    - :orange[**Programming**]: Python **//** Pandas **//** Sci Kit Learn **//** Numpy 
    - :orange[**Data Visualisation**]: Streamlit **//** Matplotlib // Seaborn **//** Plotly
    - :orange[**Modeling**]: Linear Regression **//** Random Forest Regressor **//** XGBoost
    - :orange[**Databases**]: MySQL
    """
)
st.write("\n")

#######################
# Second group of columns for images
#######################
cols = st.columns(3)
with cols[0]:
    st.image("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-plain.svg", width=50)
with cols[1]:
    st.image("https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-plain-wordmark.svg", width=50)
with cols[2]:
    st.image("https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg", width=50)