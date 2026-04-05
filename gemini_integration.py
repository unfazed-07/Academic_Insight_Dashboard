import google.generativeai as genai

def explain_performance(api_key, data):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

    prompt = f"""
You are a strict academic analyst.

Analyse the Student performance from both aspects, specific and Batch comparison.

Give:
1. Strengths
2. Weakness
3. Trend
4. Suggestion
- Keep each one in different paragraph writing paragrph name as heading above

Be specific and data-driven. keep under it concise under 2-4 line each paragraph.

Student Name: {data['student_name']}
Student CGPA {data['cgpa']}
Batch Avg CGPA: {data['batch_avg_cgpa']} 

Best Semester: {data['best_sem']} (CGPA: {data['best_sem_cgpa']})
Worst Semester: {data['worst_sem']} (CGPA: {data['worst_sem_cgpa']}) 
    
Semester-wise comparison:
{data['comparison']}
    """

    response = model.generate_content(prompt)
    return response.text if response.text else "No analysis generated"



def generate_pdf_content(api_key, student_data):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")
    prompt = """
    Create a Stuctured Student Performance Report.

    Include.
    - Student Name, Student ID
    - CGPA
    - Best Semester
    - Worst Semester
    - Short Performance Analysis

    Data: {student_data}
"""

    response = model.generate_content(prompt)
    return response.text if response.text else "No analysis generated"
