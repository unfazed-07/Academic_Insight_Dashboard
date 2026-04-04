import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3

st.title("Academic Insights Dashboard")


conn = sqlite3.connect("Python_Project")

df = pd.read_sql("""
SELECT semester, AVG(grade_point) as avg_grade
FROM marks
GROUP BY semester
""", conn)
st.dataframe(df)


fig = px.line(df, x="semester", y="avg_grade", markers=True,
              title="Average Performance Trend")

st.plotly_chart(fig)




##########
df = pd.read_sql("""
SELECT semester, AVG(grade_point) as avg_grade
FROM marks
GROUP BY semester
""", conn)

df_students = pd.read_sql("""
SELECT DISTINCT student_id
FROM marks
""", conn)
