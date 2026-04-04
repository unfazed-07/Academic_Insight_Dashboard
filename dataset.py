import sqlite3, random, os

db_path = r"C:\Users\Divyansh Sharma\JUPYER\Python_Project\db\marks.db"

batch = "CSE-2022"
if os.path.exists(db_path):
    os.remove(db_path)
    print("🗑️ Old database deleted")


Students = [
    ("S001", "Aarav Sharma"), ("S002", "Priya Singh"), ("S003", "Rahul Verma"), 
    ("S004", "Priya Singh"), ("S005","Sneha Gupta"), ("S006", "Arjun Mehta"),
    ("S007", "Karan Joshi"),("S008", "Ananya Patel"),("S009", "Rohit Nair"),
    ("S010", "Amit Kumar"), ("S011", "Neha Rajput"), ("S013", "Vikas Chauhan"),
   ("S014", "Manish Mishra"), ("S015", "Deepak Shah"), ("S016", "Suman Gupta"),
   ("S017", "Rajest Dubey"), ("S018", "Rekha Gupta"), ("S019", "Meera Jain"),
    ("S020", "Sunil Kumar"), ("S021", "Harish Sharma"), ("S022", "Shanti Jain"),
    ("S023", "Usha Iyer"), ("S024", "Dinesh Garg"), ("S025", "Harsh Mishra")
]

Semester_subjects = {
    1: [("Mathematics-I", 4), ("Physics", 3), ("Programming in C", 4) ,
        ("English Communication - I", 4), ("Engineering Design", 3), ("Cloud Fundamentals", 3)],
    2: [("Mathematics - II", 5), ("DSA - I", 5), ("Python Programming", 4),
        ("Design Thinking", 3), ("English Communication - II", 4)],
    3: [("Discrete Mathematics", 3), ("DBMS", 4), ("Computer Networks", 3),
        ("Software Engineering", 4), ("Operating Systems", 3)],
    4: [("AI Fundamentals", 4), ("Web Development", 4), ("DSA-II", 5),
        ("Statistics", 3), ("Data Engineering", 4)],
    5: [("Machine Learning", 5),("Cloud Security", 3), ("Big Data", 3),
        ("Information Security", 3), ("Object-Oriented Programming", 4)]
}

Grade_map = {
    10: "O+",
    9: "A+",
    8: "A",
    7: "B+",
    6:"B",
    5:"C",
    4:"F"
}

def assign_grade(base):
    gp = random.choices(
        [10,9,8,7,6,5,4], 
        weights = [
            max(0, base-75),
            max(0, base - 55),
            max(0, base - 45),
            max(0, base - 30),
            max(0, base - 75),
            max(0, base - 77),
            max(0, 70-base)
        ]
    )[0]
    return gp, Grade_map[gp]


os.makedirs("db", exist_ok = True)
conn = sqlite3.connect("Python_Project")
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        batch TEXT NOT NULL
    );
                  
    CREATE TABLE IF NOT EXISTS marks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        semester INTEGER NOT NULL,
        subject_name TEXT NOT NULL,
        credit_points INTEGER NOT NULL,
        grade_point REAL NOT NULL,
        grade TEXT NOT NULL
    );
""")

cur.executemany(
    "INSERT OR IGNORE INTO students VALUES (?,?,?)",
    [(sid, name, batch) for sid, name in Students]
)

rows = []
for sid, name in Students:
    base = random.randint(55, 98)

    for sem, subjects in Semester_subjects.items():
        for subject, credits in subjects:
            gp, grade = assign_grade(base)
            rows.append((sid, name, sem, subject, credits, gp, grade))

cur.executemany(
    "INSERT INTO marks (student_id, student_name, semester, subject_name, credit_points, grade_point, grade) VALUES (?,?,?,?,?,?,?)", rows
)

conn.commit()
conn.close()
print(f" {len(rows)} rows inserted. ")
