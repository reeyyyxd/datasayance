import streamlit as st
import folium
from streamlit_folium import st_folium
import time



st.set_page_config(
    page_title='My Profile | Rey',

)

st.sidebar.title("My Profile")
options = st.sidebar.radio("Go to", ["👤 About Me", "📁 My Projects"])


if options == "👤 About Me":

    with st.spinner(text="In progress"):
        time.sleep(1.5)



    st.header("Hello!")

    col1, col2 = st.columns(2)
    col1.write("Name: **Rey Anthony Montalvo Novero**")
    col1.write("Course and Year: **BS Information Technology - 4th**")
    col1.write("Hometown: **454 CPG North Avenue, Tagbilaran City, Bohol**")

    m = folium.Map(location=[9.655750, 123.855698], zoom_start=15)
    folium.Marker([9.655750, 123.855698], popup="My Hometown").add_to(m)

    with col1:
        st_folium(m, width=350, height=200)

    col2.image('img/picture.jpg')
    st.write('---')

    st.subheader("Educational Background")
    st.write("""
    - **Current** – Cebu Institute of Technology University (BS Information Technology)
    - **2019-2021** – Tagbilaran City Science High School (TVL – Information Communications Technology)
    - **2015-2019**  – Immaculate Heart of Mary Seminary
    - **2009-2015** - Saint Therese School of Mansasa
    - **2007-2009** - Saint Therese School of Gallares
    """)

    st.subheader("Hobbies")
    st.write("""
         - Film making
         - Photography
         - Exloration
         - Reading
         - Writing
        """)


    st.subheader("My Introduction Video")
    video_file = open("img/intro.mp4", "rb")
    video_bytes = video_file.read()

    st.video(video_bytes)




elif options == "📁 My Projects":

    with st.spinner(text="In progress"):
        time.sleep(1.5)




    st.header("Some Projects")
    st.write("Here are some of the projects I've worked on:")


    st.subheader("Project in CSIT284 - AcadZone")
    st.write("""
    This project is about a utility tool for students to focus on their academics. Language used is **Java**.
    """)
    st.markdown("[View Project](https://github.com/reeyyyxd/AcadZone)")

    st.subheader("Project in CSIT321 - Attendify")
    st.write("""
    This project is about an event and attendance tracker for CIT-U students and event organizers. Language used are 
    **Java Springboot, React JS and SQL**.
    """)
    st.markdown("[View Frontend](https://github.com/reeyyyxd/attendify)")
    st.markdown("[View Backend](https://github.com/reeyyyxd/DabatosNabuaNovero)")


    st.subheader("Project in CSIT327 - JJRRE Clothing Line")
    st.write("""
    This project is about an online clothing shop and. Language used are 
    **Python Flask and SQL**.
    """)
    st.markdown("[View Project](https://github.com/reeyyyxd/IM2ClothingLine)")

    st.subheader("Project in IT342 - CIT-U Inventory Management Portal")
    st.write("""
         This project is about operating all materials inside CIT-U and can monitor, request and receive materials. Language used are 
       **Java Springboot, React JS and SQL**.
         """)
    st.markdown("[View Frontend](https://github.com/reeyyyxd/CIMP_FrontEnd)")
    st.markdown("[View Backend](https://github.com/reeyyyxd/CIMP_BackEnd)")

    st.subheader("Project in CSIT349 - OpenCV and NLP")
    st.write("""
      In OpenCV, this project is about hand volume controls to your device. The NLP Project is about creating a virtual assistant
       named Arthuria. Language used is **Python**
      """)
    st.markdown("[View Project](https://github.com/EllanJ/AppliedAIProject)")

    st.subheader("Project in IT332 - Currently Working on it...")
    st.write("""
          pls give us idea huhu
          """)