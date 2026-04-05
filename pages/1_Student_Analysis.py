import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

from gemini_integration import explain_performance
from gemini_integration import generate_pdf_content

conn = sqlite3.connect("Python_Project")
df_students = pd.read_sql("SELECT DISTINCT student_id, student_name FROM marks", conn)
#############
df_students["display"] = df_students["student_name"] + " (" + df_students["student_id"].astype(str) + ")"
student = st.selectbox(
    "🎓 Select Student",
    df_students["display"])
############
############
############
student_id = student.split("(")[-1].replace(")", "")

df_info = pd.read_sql(f"""
    SELECT DISTINCT student_name
    FROM marks
    WHERE student_id = '{student_id}'
""", conn)

df_student_full_datails = pd.read_sql(f"""
    SELECT semester, grade_point FROM marks
    WHERE student_id = '{student_id}'
""", conn)
############
# CAlculated CGpa
cgpa = df_student_full_datails["grade_point"].mean()
#Calculated Best semester
sem_avg = df_student_full_datails.groupby("semester")["grade_point"].mean()
best_sem = sem_avg.idxmax()
best_sem_cgpa = sem_avg.max()
# Finding Worst Semester
worst_sem = sem_avg.idxmin()
worst_sem_cgpa = sem_avg.min()

# Overall Review
if cgpa >= 8:
    review = "Excellent"
elif cgpa >= 7.5:
    review = "Very Good"
elif cgpa >= 7.0:
    review = "Average"
elif cgpa >= 6.5:
    review = "Below Average"
else:
    review = "Poor"
#Finding highest and lowest grade
highest_grade = df_student_full_datails["grade_point"].max()
lowest_grade = df_student_full_datails["grade_point"].min()
#############
#############
student_name = df_info.iloc[0]["student_name"]
st.subheader("Student Summary")
st.write(f"Student Name: {student_name}")
st.write(f"Student ID: {student_id    }")
# Creating those 6 Boxes
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"""CGPA: {round(cgpa, 2)}     
    .
    """)
with col2:
    st.info(f"""Best Semester: {best_sem} CGPA  
    Semester CGPA: {round(best_sem_cgpa,1)}""")
with col3:
    st.info(f"""Worst Semester: {worst_sem} CGPA  
    Semester CGPA: {round(worst_sem_cgpa,1)}""")


col4, col5, col6 = st.columns(3)
with col4:
    st.info(f"Overall:\n {review}")
with col5:
    st.info(f"Max Grade {highest_grade}")
with col6:
    st.info(f"Min Grade {lowest_grade}")

#############
#############
if student:
    df_avg = pd.read_sql("""
    SELECT semester, AVG(grade_point) as avg_grade
    FROM marks
    GROUP BY semester
    """, conn)

    df_student = pd.read_sql(f"""
    SELECT semester, AVG(grade_point) as student_avg
    FROM marks
    WHERE student_id = '{student_id}'
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

#### Creating a comparison dataframe
df_batch = pd.read_sql("""
SELECT semester, AVG(grade_point) as batch_avg
FROM marks
GROUP BY semester
""", conn)

df_student_sem = sem_avg.reset_index()
df_student_sem.columns = ["semester", "student_avg"]

df_compare = pd.merge(df_student, df_batch, on = "semester")

comparison = {}

for index, row in df_compare.iterrows():
    sem = f"Sem {int(row['semester'])}"
    comparison[sem] = {
        "student" : round(row["student_avg"],2),
        "batch" : round(row["batch_avg"],2)
    }
from time import time
if st.button("Explain Performance"):
    data = {
        "student_name" : student_name,
        "cgpa" : cgpa,
        "best_sem": best_sem,
        "best_sem_cgpa": best_sem_cgpa,
        "worst_sem": worst_sem,
        "worst_sem_cgpa": worst_sem_cgpa,
        "max_grade": highest_grade,
        "min_grade": lowest_grade,
        "batch_avg_cgpa": round(df_batch["batch_avg"].mean(),2),
        "comparison": comparison
    }
    with st.spinner("Analyzing performance"):
        result = explain_performance(
        st.secrets["GEMINI_API_KEY"],
        data
        )

    if result:
        st.success(result)
    else:
        st.error("No response from Gemini")


