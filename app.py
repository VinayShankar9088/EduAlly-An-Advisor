import os
from flask import Flask, request, send_from_directory, redirect, abort
import sqlite3

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__)

DB_PATH = os.path.join(BASE_DIR, "app.db")


def init_db():
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute(
		"""
		CREATE TABLE IF NOT EXISTS students (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			age INTEGER,
			class TEXT,
			stream TEXT,
			location TEXT,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
		"""
	)
	conn.commit()
	conn.close()


def serve_file(relpath):
	# Protect path traversal and ensure file exists
	full = os.path.normpath(os.path.join(BASE_DIR, relpath))
	if not full.startswith(os.path.normpath(BASE_DIR)):
		abort(404)
	if not os.path.isfile(full):
		abort(404)
	directory, filename = os.path.split(full)
	return send_from_directory(directory, filename)


@app.route("/")
def index():
	# prefer welcome/index.html, fallback to practice.html
	if os.path.isfile(os.path.join(BASE_DIR, "welcome", "index.html")):
		return serve_file(os.path.join("welcome", "index.html"))
	if os.path.isfile(os.path.join(BASE_DIR, "practice.html")):
		return serve_file("practice.html")
	abort(404)


@app.route("/student_info")
def student_info():
	return serve_file("student_info.html")


@app.route("/Onboarding/<path:filename>")
def onboarding_files(filename):
	return serve_file(os.path.join("Onboarding", filename))


@app.route("/welcome/<path:filename>")
def welcome_files(filename):
	return serve_file(os.path.join("welcome", filename))


@app.route("/dashboard/<path:filename>")
def dashboard_files(filename):
	return serve_file(os.path.join("dashboard", filename))


@app.route("/logo_new.jpg")
def logo():
	return serve_file("logo_new.jpg")


@app.route("/save_student", methods=["POST"])
def save_student():
	# Collect fields from the submitted form
	name = request.form.get("name", "").strip()
	age = request.form.get("age")
	student_class = request.form.get("class")
	stream = request.form.get("stream")
	location = request.form.get("location")

	if not name:
		return "Missing student name", 400

	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute(
		"INSERT INTO students (name, age, class, stream, location) VALUES (?,?,?,?,?)",
		(name, age, student_class, stream, location),
	)
	conn.commit()
	conn.close()

	# After saving, redirect to dashboard
	return redirect("/dashboard/dashboard.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

