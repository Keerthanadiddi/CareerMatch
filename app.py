from os import name
import sqlite3
from webbrowser import get

from flask import Flask,render_template,request
app=Flask(__name__)
def get_db_connection():
   conn=sqlite3.connect('database.db')
   conn.row_factory=sqlite3.Row
   return conn
def create_tables():
   conn=get_db_connection()
   conn.execute('''
       CREATE TABLE IF NOT EXISTS internships (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           title TEXT NOT NULL,
           company TEXT NOT NULL,
           description TEXT
       )
   ''')
   conn.execute('''
       CREATE TABLE IF NOT EXISTS skills (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL
       )
   ''')
   conn.execute('''
       CREATE TABLE IF NOT EXISTS profiles (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           email TEXT NOT NULL           
       )
   ''')
   columns=conn.execute("PRAGMA table_info(profiles)").fetchall()
   if "college" not in [column["name"] for column in columns]:
        conn.execute("ALTER TABLE profiles ADD COLUMN college TEXT NOT NULL")
   conn.commit()
   conn.close()
def add_sample_internships():
    conn = get_db_connection()

    internships = [
        (
            "Python Developer Intern",
            "ABC Technologies",
            "Work on Python applications and backend development."
        ),
        (
            "Data Science Intern",
            "XYZ Analytics",
            "Work with Python, Pandas, NumPy and data analysis."
        ),
        (
            "Java Developer Intern",
            "Tech Solutions",
            "Develop Java applications and work with databases."
        ),
        (
            "AI/ML Intern",
            "Innovate AI",
            "Work on machine learning projects using Python."
        )
    ]
    for internship in internships:
        conn.execute("""
            INSERT INTO internships (title, company, description)
            VALUES (?, ?, ?)
        """, internship)
    
    conn.commit()
    conn.close()
def fix_internship_data():
   conn=get_db_connection()
   conn.execute(""" 
    UPDATE internships 
    SET title=company,
    company=title
   """)  
   conn.commit()
   conn.close()
@app.route("/")
def hello():
   return render_template("index.html")
@app.route("/profile",methods=["GET","POST"])
def profile():
   if request.method=="POST":
       name=request.form["name"]
       email=request.form["email"]
       college=request.form["college"]
       conn=get_db_connection()
       conn.execute("""
           INSERT INTO profiles (name, email, college)
           VALUES (?, ?, ?)
       """, (name, email, college))
       conn.commit()
       conn.close()
       return """<h2>Profile saved Successfully!</h2><a href='/profile'>Add another profile</a>"""
   return render_template("profile.html")

@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == "POST":
        name = request.form["name"].strip()

        if not name:
            return "Please enter a skill."

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO skills (name) VALUES (?)",
            (name,)
        )

        conn.commit()
        conn.close()

        return """
            <h2>Skill saved successfully!</h2>
            <a href="/skills">Add another skill</a> |
            <a href="/">Home</a>
        """

    return render_template("skills.html")


@app.route("/match")
def match():
   return render_template("match.html");
@app.route("/internships")
def internships():
   conn=get_db_connection()
   internships=conn.execute('SELECT * FROM internships').fetchall()
   conn.close()
   return render_template("internships.html", internships=internships);
@app.route("/internship_details")
def internship_details():
   return render_template("internship_details.html");
def remove_sample_internships():
    conn = get_db_connection()
    conn.execute(" " " DELETE FROM internships WHERE id NOT IN (SELECT MIN(id) FROM internships GROUP BY title,company,description)" " ")
    conn.commit()
    conn.close()
    print("Duplicate removed !")
if __name__=="__main__":
   create_tables()
   app.run(debug=True)
