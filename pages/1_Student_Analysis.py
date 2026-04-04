import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3


conn = sqlite3.connect("Python_Project")


df_students = pd.read_sql("SELECT DISTINCT student_id FROM marks", conn)

student = st.selectbox(
    "🎓 Select Student",
    df_students[["student_id"]]
)

if student:



    df_avg = pd.read_sql("""
    SELECT semester, AVG(grade_point) as avg_grade
    FROM marks
    GROUP BY semester
    """, conn)

    df_student = pd.read_sql(f"""
    SELECT semester, AVG(grade_point) as student_avg
    FROM marks
    WHERE student_id = '{student}'
    GROUP BY semester
    """, conn)

    compare_df = pd.merge(df_avg, df_student, on="semester", how="inner")

    compare_df["avg_grade"] = pd.to_numeric(compare_df["avg_grade"])
    compare_df["student_avg"] = pd.to_numeric(compare_df["student_avg"])

    fig = px.line(
        compare_df,
        x="semester",
        y=["avg_grade", "student_avg"],
        markers=True,
        title="Student vs Batch Performance"
    )

    st.plotly_chart(fig)

    st.subheader("Studnet Summary")
    st.write(f"Student ID: {student}")
    st.write(f"Student Name: {student}")

    col1, col2, col3 = st.columns(3)
