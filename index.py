from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from tkinter import messagebox
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_here'  # Change this to a strong random value in production


@app.route("/", methods=["GET"])
def index():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
    cut = mydb.cursor()
    cut.execute("SELECT * FROM tasks")
    records = cut.fetchall()
    cut.close()
    mydb.close()
    return render_template('dashboard.html', records=records)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)

        # Create main database if not exists
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='')
        cut = mydb.cursor()
        cut.execute(f"CREATE DATABASE IF NOT EXISTS task_manager")
        cut.close()
        mydb.close()

        # Connect to the main database and create tables
        mydb2 = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
        cut2 = mydb2.cursor()
        cut2.execute('''CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(255) UNIQUE NOT NULL,
            Password VARCHAR(255) NOT NULL
        )''')
        cut2.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            Task_Name VARCHAR(255),
            Status VARCHAR(50),
            Task_Description TEXT(500),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )''')
        # Insert the new user
        cut2.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mydb2.commit()
        cut2.close()
        mydb2.close()
        return render_template('login.html')
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
        cut = mydb.cursor()
        cut.execute("SELECT password FROM users WHERE username=%s", (username,))
        result = cut.fetchone()
        cut.close()
        mydb.close()

        if result and check_password_hash(result[0], password):
            # Login successful
            mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
            cut = mydb.cursor()
            cut.execute("SELECT * FROM tasks")
            records = cut.fetchall()
            cut.close()
            mydb.close()
            return render_template('dashboard.html', records=records)
        else:
            # Login failed
            flash('Invalid username or password')
            return render_template('login.html')
    # For GET requests, show dashboard
    return render_template('login.html')

@app.route("/add_item", methods=['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        comment = request.form['comment']
        mydb3 = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
        cut3 = mydb3.cursor()
        insert_sql = "INSERT INTO tasks (Task_Name, Status, Task_Description) VALUES (%s, %s, %s)"
        cut3.execute(insert_sql, (name, 'Pending', comment))
        mydb3.commit()
        cut3.close()
        mydb3.close()
        return redirect(url_for('index'))
    # For GET requests, show dashboard
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
    cut = mydb.cursor()
    cut.execute("SELECT * FROM tasks")
    records = cut.fetchall()
    cut.close()
    mydb.close()
    return render_template('dashboard.html', records=records)
# Route to handle form submission and create database
@app.route("/create_db", methods=["POST"])
def create_db():
    db_name = request.form.get("name")
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='')
    cursor = mydb.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
    mydb.close()
    return redirect(url_for("index"))

@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    status = request.form.get('status', 'Pending')
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
    cut = mydb.cursor()
    cut.execute("UPDATE tasks SET Status=%s WHERE id=%s", (status, task_id))
    mydb.commit()
    cut.close()
    mydb.close()
    return ('', 204)

@app.route('/add_task', methods=['GET'])
def add_task():
    return render_template('add_task.html')

@app.route('/edit_task/<int:task_id>', methods=['GET'])
def edit_task(task_id):
    mydb2 = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
    cut2 = mydb2.cursor()
    cut2.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    record = cut2.fetchone()
    cut2.close()
    mydb2.close()
    return render_template('edit.html', record=record)

@app.route('/edit_item', methods=['POST'])
def edit_item():
    task_id = request.form.get('id')
    title = request.form.get('name')
    comm = request.form.get('comment')
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
    cut = mydb.cursor()
    cut.execute("UPDATE tasks SET Task_Name=%s, Task_Description=%s WHERE id=%s", (title, comm, task_id))
    mydb.commit()
    cut.close()
    mydb.close()
    return redirect(url_for('index'))

@app.route('/dash')
def dash():
    let = index()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='task_manager')
    cut = mydb.cursor() 
    cut.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    mydb.commit()
    cut.close()
    mydb.close()
    return redirect(url_for('index'))

@app.route("/log_out", methods=["GET"])
def logout():
    # Logic for logging out the user
    return redirect(url_for('register'))

@app.route('/take')
def take():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)