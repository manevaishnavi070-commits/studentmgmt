# import SQLite
# from flask import Flask, render_template, request, redirect
# import sqlite3

# connection = sqlite3.connect("students.db")
# cursor = connection.cursor()
# cursor.execute(""" 
#                CREATE TABLE IF NOT EXISTS students
#                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
#                name TEXT, 
#                age INTEGER ,
#                course TEXT,    
#                city TEXT)
#                """)

# connection.commit()
# connection.close()



# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")



# @app.route("/add", methods=["POST"])

# def add():

#     name = request.form["name"]

#     age = request.form["age"]

#     course = request.form["course"]

#     city = request.form["city"]

#     connection = sqlite3.connect("students.db")

#     cursor = connection.cursor()

#     cursor.execute("""

#     INSERT INTO students

#     (name, age, course, city)
#     VALUES (?, ?, ?, ?)

#     """,
#     (name, age, course, city)

#     )

#     connection.commit()

#     connection.close()

#     return redirect("/")




# @app.route("/students")

# def students():

#     connection = sqlite3.connect("students.db")

#     cursor = connection.cursor()

#     cursor.execute("SELECT * FROM students")

#     data = cursor.fetchall()

#     connection.close()
#     return render_template("students.html",students=data)

# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, render_template, request, jsonify
import sqlite3


app = Flask(__name__)

DATABASE = "students.db"


# ==========================
# DATABASE CONNECTION
# ==========================

def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection



# ==========================
# CREATE TABLE
# ==========================

def create_table():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

    CREATE TABLE IF NOT EXISTS students(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        age INTEGER NOT NULL,

        course TEXT NOT NULL,

        city TEXT NOT NULL

    )

    """)


    connection.commit()

    connection.close()



create_table()



# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    return render_template("index.html")



# ==========================
# GET STUDENTS
# ==========================

@app.route("/api/students", methods=["GET"])
def get_students():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        "SELECT * FROM students ORDER BY id DESC"
    )


    rows = cursor.fetchall()


    connection.close()


    students = []


    for row in rows:

        students.append(dict(row))


    return jsonify(students),200





# ==========================
# ADD STUDENT
# ==========================


@app.route("/api/students", methods=["POST"])
def add_student():

    data=request.get_json()


    if not data:

        return jsonify({

            "message":"No data received"

        }),400



    name=data.get("name")
    age=data.get("age")
    course=data.get("course")
    city=data.get("city")



    if not name or not age or not course or not city:

        return jsonify({

            "message":"All fields required"

        }),400



    connection=get_connection()

    cursor=connection.cursor()



    cursor.execute("""

    INSERT INTO students(name,age,course,city)

    VALUES(?,?,?,?)

    """,

    (name,age,course,city)

    )



    connection.commit()


    connection.close()



    return jsonify({

        "message":"Student Added Successfully"

    }),201





# ==========================
# UPDATE STUDENT
# ==========================


@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):


    data=request.get_json()



    if not data:

        return jsonify({

            "message":"No Data Received"

        }),400



    connection=get_connection()

    cursor=connection.cursor()



    cursor.execute("""

    UPDATE students

    SET name=?,
        age=?,
        course=?,
        city=?

    WHERE id=?


    """,

    (

    data.get("name"),
    data.get("age"),
    data.get("course"),
    data.get("city"),
    id

    )

    )



    connection.commit()



    if cursor.rowcount==0:


        connection.close()


        return jsonify({

            "message":"Student Not Found"

        }),404



    connection.close()



    return jsonify({

        "message":"Student Updated Successfully"

    }),200





# ==========================
# DELETE STUDENT
# ==========================


@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):


    connection=get_connection()

    cursor=connection.cursor()



    cursor.execute(

        "DELETE FROM students WHERE id=?",

        (id,)

    )


    connection.commit()



    if cursor.rowcount==0:


        connection.close()


        return jsonify({

            "message":"Student Not Found"

        }),404




    connection.close()



    return jsonify({

        "message":"Student Deleted Successfully"

    }),200





# ==========================
# RUN APPLICATION
# ==========================


if __name__=="__main__":

    app.run(debug=True)