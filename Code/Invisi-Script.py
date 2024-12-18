import streamlit as st
from TextEditor import text_editor
from AirCanvas import air_canvas
col1,col2 =st.columns([4,1])
with col1:
    st.markdown(
    "<h1 style='text-align:left; font-size=56'>INVISI-SCRIPT</h1>",
    unsafe_allow_html=True
    )



col3,col4 = st.columns([4,5])

#with st.container(height=700,border=True):
st.markdown(
    """
    <style>
   
    .custom-co2 {
        width: 70% !important;  
        margin: auto; 
    }
    </style>
    """,
    unsafe_allow_html=True
)
extracted_text =""
with col3:
    text_editor(extracted_text)
with col4:
    air_canvas()