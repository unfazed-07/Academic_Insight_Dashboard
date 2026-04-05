import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3

st.set_page_config(layout="wide")
st.title("Academic Insights Dashboard")
conn = sqlite3.connect("Python_Project")

df_performance = pd.read_sql("""
    SELECT student_id,student_name, AVG(grade_point) as avg_grade
    FROM marks
    GROUP BY student_id
""", conn)

top_3 = df_performance.sort_values(by = "avg_grade", ascending=False).head(3)
st.subheader("Top Performers")
for i , row in top_3.iterrows():
    st.success(f"{row['student_name']} -> {round(row['avg_grade'],2)}")

df = pd.read_sql("""
SELECT semester, AVG(grade_point) as avg_grade
FROM marks
GROUP BY semester
""", conn)

col1, col2 = st.columns(2)
with col1:
    
    fig = px.line(df, x="semester", y="avg_grade", markers=True,
                title="Average Performance Trend")

    st.plotly_chart(fig)

with col2:
    df_all = pd.read_sql("SELECT grade_point FROM marks", conn)

    fig2, ax = plt.subplots(figsize=(8,5))

    fig2.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#0E1117')

    ax.hist(df_all["grade_point"], bins=10)

    ax.set_xlabel("Grade Points")
    ax.set_ylabel("Number of Students")
    ax.set_title("Distribution of Grades")

    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')

    st.pyplot(fig2)