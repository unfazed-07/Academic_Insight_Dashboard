import streamlit as st

st.title("About This Project")
st.write("""
    This Academic Insight Dashboard helps visualize and analyse
    academic performance using interactive charts and key matrices.
         
    It allows comparisn with bath performance and provides insights into trends.
""")


st.subheader("Features")
st.write("""
- Student-wise performance tracking
- Semester comparison
- Batch vs Individual analysis
- Performance insights
""")

st.subheader("Limitations")
st.write("""This project is made as a college-level project to show basic data
          analysis and visualization skills.
          It works only on a fixed dataset and does not support data from
          external sources like SQL, Excel, or CSV files.
          It is not a production-level application.""")

st.subheader("Tech Stacks Used")
st.write("""
- Python - Language used to build Togic of this project
- Streamlit - Used to create the web interface and all the visuals
- Pandas - Helps in handeling and analyse the dataset
- SQLite - Used as create an manage Sturctured Data.
- Plotty - Used to create charts and visualizations for better understanding todata
- Gemini Api - Used to generate summarize student-specific insights.
""")

st.subheader("Team Members")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    👤**Ujwal UK**  
    [LinkedIn](https://www.linkedin.com/in/ujwal-u-k-9428a6381/)
    """)

with col2:
    st.markdown("""
    👤**Rohit Rejikumar**  
    [LinkedIn](https://www.linkedin.com/in/ujwal-u-k-9428a6381/)
    """)

col3 , col4= st.columns(2)

with col3:
    st.markdown("""
    👤**Avinash Singh**  
    @------
    """)

with col4:
    st.markdown("""
    👤**Divyansh Sharma**  
    [LinkedIn](https://www.linkedin.com/in/divyansh-sharma-5546b3223/)
    """)