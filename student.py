from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/save_student', methods=['POST'])
def save_student():
    name = request.form['name']
    age = request.form['age']
    student_class = request.form['class']
    stream = request.form['stream']
    location = request.form['location']

    # Save in database
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, age, class, stream, location) VALUES (?,?,?,?,?)",
              (name, age, student_class, stream, location))
    conn.commit()
    conn.close()

    # Redirect to college suggestion page
    return f"Hello {name}, we will suggest colleges in {location} for {stream}!"

if __name__ == "__main__":
    app.run(debug=True)
